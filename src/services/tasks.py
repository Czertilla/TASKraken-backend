from logging import getLogger
from uuid import UUID
from models.tasks import TaskORM
from schemas.filters.roles import RoleFilter
from models.roles import RoleORM
from models.structures import StructureORM
from models.users import UserORM
from schemas.pagination import SPaginationRequest, SPaginationResponse
from schemas.projects import SMyProjectsResponse, SMyTasksresponse, STaskPreview
from schemas.roles import SRolePreview, SRoleRights
from schemas.structures import SCreateStruct, SCreateStructResponse, SRegistOrgResponse, SRegistOrganization
from utils.absract.service import BaseService
from utils.enums.rights import CreateStructRight, SendTaskVector

logger = getLogger(__name__)

class TaskService(BaseService):
    async def can_send_task_to_recipient(
        self,
        adresser: RoleORM,
        recipient: RoleORM
    ) -> bool:
        match adresser.rights.can_send_task:
            case SendTaskVector.everyone:
                return True
            case SendTaskVector.organization:
                return (
                    adresser.structure.org_id ==
                    recipient.structure.org_id
                )
            case SendTaskVector.structure:
                return (
                    adresser.structure_id ==
                    recipient.structure_id
                )
            case SendTaskVector.downstream:
                return await self.uow.roles.is_on_downstream(adresser.id, recipient.id)
            case SendTaskVector.direct_down:
                return (
                    adresser.id ==
                    recipient.chief_id
                )
            case _:
                return False


    async def can_send_task(
        self,
        addresser_id: UUID,
        recipients: list[UUID]
    ) -> list[SRolePreview]:
        async with self.uow:
            addresser: RoleORM = await self.uow.roles.get_with_rights(addresser_id)
            recipients: list[UserORM] = await self.uow.roles.search(RoleFilter(id__in=recipients))
            return [ 
                role if await self.can_send_task_to_recipient(addresser, role) else ...
                for role in recipients
            ]


    async def get_tasks_by_creator_id(
        self,
        creator_id: UUID,
        pagination: SPaginationRequest
    ) -> SMyProjectsResponse:
        async with self.uow:
            role: RoleORM = await self.uow.roles.get_with_assignments(creator_id)
            tasks_list = role.created_tasks
            await self.uow.commit(flush=True)
        return self.get_tasks_list_response(tasks_list, pagination)


    async def get_tasks_by_responsobility_id(
        self,
        respons_id: UUID,
        pagination: SPaginationRequest
    ) -> SMyProjectsResponse:
        async with self.uow:
            role: RoleORM = await self.uow.roles.get_with_tasks(respons_id)
            tasks_list = role.tasks
            await self.uow.commit(flush=True)
        return self.get_tasks_list_response(tasks_list, pagination)


    def get_tasks_list_response(
        self,
        tasks_list: list[TaskORM],
        pagination: SPaginationRequest
    ) -> SMyTasksresponse:
        offset = self.get_offset(pagination)
        return SMyProjectsResponse(
            result=[
                STaskPreview(
                    id=task.id,
                    name=task.name,
                    creator_id=task.creator_id,
                    description=(text:=task.desctription)[:STaskPreview._description_limit]+
                        ("..." if len(text) <= STaskPreview._description_limit else ''),
                    created_at=task.created_at,
                    edited_at=task.edited_at
                ) for task in tasks_list[offset[0]:offset[1]]
            ],
            pagination=SPaginationResponse(
                page=pagination.page,
                size=pagination.size,
                total=self.get_total_pagination(len(tasks_list), pagination.size))
        )


    async def create_task(self):
        ...