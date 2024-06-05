from logging import getLogger
from typing import Annotated
from uuid import UUID

from fastapi import Cookie, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from models.users import UserORM
from schemas.filters.roles import RoleFilter
from models.files import FileORM, FolderORM
from models.roles import RoleORM
from models.tasks import ProjectORM, TaskORM
from schemas.pagination import SPaginationRequest, SPaginationResponse
from schemas.projects import SCreateProjectRequest, SCreateProjectResponse, SCreateTaskRequest, SCreateTaskResponse, SMyProjectsResponse, SProjectCheckResponce, SProjectPreview
from schemas.roles import SRolePreview
from utils.absract.service import BaseService
from utils.enums.projects import CheckProjectStatus
from utils.enums.task import TaskStatus


logger = getLogger(__name__)


class ProjectService(BaseService):
    async def can_edit_project(
        self,
        role_id: UUID,
        project_id: UUID,
        get_mode: bool = False
    ) -> ProjectORM|CheckProjectStatus:
        async with self.uow:
            project = await self.uow.projects.get(project_id)
            role = await self.uow.roles.get(role_id)
            if type(project) != ProjectORM:
                return CheckProjectStatus.unexist
            if type(role) != RoleORM:
                return CheckProjectStatus.unbelonged
            if project.creator_id == role.id:
                if get_mode:
                    await self.uow.commit(flush=True)
                    return project
                return CheckProjectStatus.belong
            else:
                return CheckProjectStatus.unbelonged
        return CheckProjectStatus.__default__


    async def get_project_cookie(
        self,
        role_id: UUID,
        project_id: UUID
    ) -> JSONResponse:
        if type(project:= await self.can_edit_project(role_id, project_id, get_mode=True)) == ProjectORM:
            content = self.get_project_preview(project).model_dump(mode="json")
            response = JSONResponse(content=content)
            response.set_cookie(key="project_id", value=project_id)
            return response
        else:
            raise HTTPException(
                status_code=422, 
                detail=SProjectCheckResponce(
                    request_key="project_id",
                    role_id=project_id,
                    status=project
                ).model_dump(mode="json")
            )
    

    def get_project_preview(
        self,
        project: ProjectORM
    ) -> SProjectPreview:
        return SProjectPreview(
            id=project.id,
            name=project.name,
            organization_id=project.organization_id,
            description=(text:=project.desctription)[:SProjectPreview._description_limit]+
                ("..." if len(text) <= SProjectPreview._description_limit else ''),
            created_at=project.created_at,
            edited_at=project.edited_at
        )


    async def get_project_by_creator_id(
        self,
        creator_id: UUID,
        pagination: SPaginationRequest
    ) -> SMyProjectsResponse:
        async with self.uow:
            role: RoleORM = await self.uow.roles.get_for_projects(creator_id)
            offset = self.get_offset(pagination)
            return SMyProjectsResponse(
                result=[
                    self.get_project_preview(project) 
                    for project in (role.created_projects)[offset[0]:offset[1]]
                ],
                pagination=SPaginationResponse(
                    page=pagination.page,
                    size=pagination.size,
                    total=self.get_total_pagination(len(role.created_projects), pagination.size))
            )


    async def create_project(
        self, 
        role_id: UUID, 
        request: SCreateProjectRequest
    ) -> SCreateProjectResponse:
        async with self.uow:
            role: RoleORM = await self.uow.roles.get_for_page(role_id)
            if role.rights is None:
                raise HTTPException(code_status=422, detail=f"cannot find rights for role {role_id}")
            if not role.rights.can_create_project:
                raise HTTPException(status_code=403, detail=f"role {role_id} has not right")
            request_data: dict = request.model_dump()
            request_data.update({
                "organization_id": role.structure.org_id if role.structure.org_id else role.structure_id,
                "creator_id": role.id,

            })
            id: UUID = await self.uow.projects.add_one(request_data)
            status: TaskStatus = await self.uow.projects.get_status(id)
            request_data.update({
                "id": id,
                "status": status.value
            })
            await self.uow.commit()
        return SCreateProjectResponse(**request_data)


    async def add_task(
        self,
        role_id: UUID,
        request: SCreateTaskRequest,
        project_id: UUID
    ) -> SCreateTaskResponse:
        async with self.uow:
            role: RoleORM = await self.uow.roles.get_for_page(role_id)
            project: ProjectORM = await self.uow.projects.get(project_id)
            if role.id != project.creator_id:
                raise HTTPException(
                    status_code=403, 
                    detail=f"project {project_id} doesn`t belong to role {role_id}"
                )
            data: dict = request.model_dump()
            # files: list[UploadFile] = data.pop("files")
            # TODO implement
            # if files:
            #     folder: FolderORM = await self.uow.folders.add_n_return({})
            #     for file in files:
            #         folder.files.append(FileORM(
            #             name = file.filename,
            #             data = await file.read()
            #         ))
            #     await self.uow.folders.merge(folder)
            #     data.update({"folder_id": folder.id})
            checklists: list[dict] = data.pop("checklists")
            if checklists:
                ...
            data.update({"creator_id": role_id, "project_id": project_id})
            resp_id_list: list[UUID] = data.pop("responsobilities")
            task: TaskORM = TaskORM(**data)
            task: TaskORM = await self.uow.tasks.add_n_return(data)
            responsibles: list[RoleORM] = await self.uow.roles.search(RoleFilter(id__in=resp_id_list))
            for responsible in responsibles:
                task.responsibles.append(responsible)
            await self.uow.commit(flush=True)
        return SCreateTaskResponse(
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
