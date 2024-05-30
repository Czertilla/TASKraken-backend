from logging import getLogger
from uuid import UUID

from fastapi import HTTPException, UploadFile
from models.files import FileORM, FolderORM
from models.tasks import TaskORM
from schemas.filters.roles import RoleFilter
from models.roles import RoleORM
from models.structures import StructureORM
from models.users import UserORM
from schemas.pagination import SPaginationRequest, SPaginationResponse
from schemas.projects import SAddCheckList, SMyProjectsResponse, SMyTasksresponse, STaskPage, STaskPreview
from schemas.roles import SRoleCheckResponce, SRolePreview, SRoleRights
from schemas.structures import SCreateStruct, SCreateStructResponse, SRegistOrgResponse, SRegistOrganization
from utils.absract.service import BaseService
from utils.enums.rights import CreateStructRight, SendTaskVector
from utils.enums.task import TaskViewMode

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

    
    async def can_watch_task(
        self,
        watcher_id: UUID,
        task_id: UUID,
        task: TaskORM|None = None
    ) -> bool:
        async with self.uow:
            if isinstance(task, TaskORM):
                return task.project.organization_id


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


    async def create_task(
        self,
        creator_id: UUID,
        request: SCreateSubTaskRequest # type: ignore
    ) -> SCreateSubTaskResponse: # type: ignore
        async with self.uow:
            role: RoleORM = await self.uow.roles.get_for_page(creator_id)
            overtask: TaskORM = await self.uow.tasks.get(request.fromtask_id)
            if overtask.id not in role.tasks:
                raise HTTPException(
                    status_code=403, 
                    detail=f"role {creator_id} isn`t responsible of task {overtask.id}"
                )
            data: dict = request.model_dump()
            files: list[UploadFile] = data.pop("files")
            if files:
                folder: FolderORM = await self.uow.folders.add_n_return({})
                for file in files:
                    folder.files.append(FileORM(
                        name = file.filename,
                        data = await file.read()
                    ))
                await self.uow.folders.merge(folder)
                data.update({"folder_id": folder.id})
            checklists: list[dict] = data.pop("checklists")
            if checklists:
                # TODO implement
                ...
            data.update({"creator_id": creator_id})
            resp_id_list: list[UUID] = data.pop("responsobilities")
            task: TaskORM = TaskORM(**data)
            task: TaskORM = await self.uow.tasks.add_n_return(data)
            responsibles: list[RoleORM] = await self.uow.roles.search(RoleFilter(id__in=resp_id_list))
            for responsible in responsibles:
                task.responsibles.append(responsible)
            await self.uow.commit(flush=True)
        return SCreateSubTaskResponse( # type: ignore
            id=task.id,
            name=task.name,
            desctription=task.desctription,
            deadline=task.deadline,
            creator_id=task.creator_id,
            status=task.status.value,
            responsobilities=[
                SRolePreview(
                    id=role.id,
                    name=role.name,
                    level=role.level
                ) for role in task.responsibles
            ],
            level=task.level
        )


    async def get_task_page(
        self,
        role_id: UUID,
        task_id: UUID
    ) -> STaskPage:
        async with self.uow:
            task: TaskORM = await self.uow.tasks.get_for_page(task_id)
            if not isinstance(task, TaskORM):
                raise HTTPException(
                status_code=422, 
            )
            if task.creator_id == role_id:
                view_mode = TaskViewMode.responsible
            elif role_id in [role.id for role in task.responsibles]:
                view_mode = TaskViewMode.creator
            else:
                view_mode = TaskViewMode.rejected
                # TODO implement rejection
            return STaskPage(
                view_mode = view_mode,
                name = task.name,
                deadline = task.deadline,
                descripition = task.desctription,
                status = task.status,
                checklists = [
                    SAddCheckList(
                        name = checklist.name,
                        checkpoints = [point for point in checklist.points]
                    ) 
                    for checklist in task.checklists
                ],
                responsobilities = [
                    SRolePreview(
                        id = role.id,
                        name = role.name
                    ) for role in task.responsibles
                ],
                # TODO implement
                # project = Annotated[SProjectPreview, Field()]
                # overtask = Annotated[STaskPreview|None, Field()]
                # subtasks = Annotated[list[STaskPreview], Field()] = []
                created_at = task.created_at,
                edited_at = task.edited_at
            )