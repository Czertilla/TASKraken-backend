from logging import getLogger
from uuid import UUID

from fastapi import HTTPException, UploadFile
from models.checklists import ChecklistORM, CheckpointORM
from models.files import FileORM, FolderORM
from models.tasks import TaskORM
from schemas.filters.roles import RoleFilter
from models.roles import RoleORM
from models.structures import StructureORM
from models.users import UserORM
from schemas.pagination import SPaginationRequest, SPaginationResponse
from schemas.projects import SAddCheckList, SCreateSubTaskRequest, SCreateSubTaskResponse, SMyProjectsResponse, SMyTasksResponse, SPutTaskRequest, STaskPage, STaskPreview, SViewChecklist, SViewCheckpoints
from schemas.roles import SRoleCheckResponce, SRolePreview, SRoleRights
from schemas.structures import SCreateStruct, SCreateStructResponse, SRegistOrgResponse, SRegistOrganization
from utils.absract.service import BaseService
from utils.enums.rights import CreateStructRight, SendTaskVector
from utils.enums.task import TaskStatus, TaskViewMode

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
            tasks_list = list(filter(lambda task: TaskStatus(task.status), role.created_tasks))
            await self.uow.commit(flush=True)
        return self.get_tasks_list_response(tasks_list, pagination)


    async def get_tasks_by_responsobility_id(
        self,
        respons_id: UUID,
        pagination: SPaginationRequest
    ) -> SMyProjectsResponse:
        async with self.uow:
            role: RoleORM = await self.uow.roles.get_with_tasks(respons_id)
            tasks_list = list(filter(lambda task: TaskStatus(task.status), role.tasks))
            await self.uow.commit(flush=True)
        return self.get_tasks_list_response(tasks_list, pagination)


    def get_tasks_list_response(
        self,
        tasks_list: list[TaskORM],
        pagination: SPaginationRequest
    ) -> SMyTasksResponse:
        offset = self.get_offset(pagination)
        return SMyTasksResponse(
            result=[
                STaskPreview(
                    id=task.id,
                    name=task.name,
                    description=(text:=task.desctription)[:STaskPreview._description_limit]+
                        ("..." if len(text) <= STaskPreview._description_limit else ''),
                    creator_name=task.creator.name,
                    deadline=task.deadline,
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
        request: SCreateSubTaskRequest 
    ) -> SCreateSubTaskResponse: 
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
                view_mode = TaskViewMode.creator
            elif role_id in [role.id for role in task.responsibles]:
                view_mode = TaskViewMode.responsible
            else:
                view_mode = TaskViewMode.rejected
                # TODO implement rejection
            return STaskPage(
                view_mode = view_mode,
                id = task.id,
                name = task.name,
                deadline = task.deadline,
                descripition = task.desctription,
                status = task.status,
                checklists = [
                    SViewChecklist(
                        id = chlst.id,
                        name = chlst.name,
                        points = [
                            SViewCheckpoints(
                                id=point.id,
                                name=point.name,
                                done=point.done
                            ) for point in chlst.checkpoints
                        ]
                    )
                    for chlst in task.checklists
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
        
    
    async def update_checklists(
        self,
        task: TaskORM,
        checklists: list[SViewChecklist]
    ) -> None:
        # TODO implement deletion by ignore
        for chlst in checklists:
            data = chlst.model_dump()
            if chlst.id is None or (checklist := await self.uow.checklists.get(chlst.id) is None):
                task.checklists.append(await self.uow.checklists.add_n_return(data))
            elif isinstance(checklist, ChecklistORM):
                checklist.name = chlst.name
                for pnt in chlst.points:
                    if (
                        pnt.id is None or 
                        (
                            point:= await self.uow.checklists.get_point(
                                pnt.id, 
                                chlst.id
                            ) is None
                        )
                    ):
                        self.uow.checklists.add_point(point, chlst.id)
                    elif isinstance(point, CheckpointORM):
                        point.name = pnt.name
                        point.done = pnt.done
        ...

    async def put_task(
        self,
        role_id: UUID,
        task_data: SPutTaskRequest,
    ) -> STaskPage:
        async with self.uow:
            task: TaskORM = await self.uow.tasks.get_for_page(task_data.id)
            if not isinstance(task, TaskORM):
                raise HTTPException(
                    status_code=422, 
                )
            if task.creator_id == role_id:
                view_mode = TaskViewMode.creator
            elif role_id in [role.id for role in task.responsibles]:
                view_mode = TaskViewMode.responsible
            else:
                view_mode = TaskViewMode.rejected
                # TODO implement rejection
            if view_mode != task_data.view_mode:
                raise HTTPException(
                    status_code=403, 
                )
            if view_mode in {TaskViewMode.responsible, TaskViewMode.creator}:
                await self.update_checklists(task, task_data.checklists)
                # TODO implements files
            if view_mode == TaskViewMode.creator:
                task.name = task_data.name
                task.desctription = task_data.descripition
                task.status = task_data.status
                task.deadline = task_data.deadline
                # TODO implement
                # task.responsibles = task_data.responsobilities
                # subtasks : Annotated[list[STaskPreview], Field()] = []=
            await self.uow.commit()
        return await self.get_task_page(role_id, task_data.id)