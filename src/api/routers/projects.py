
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from api.dependencies import ProjectUOWDep, ProjectUUID, RoleUUID
from api.auth.auth import fastapi_users
from models.users import UserORM
from schemas.pagination import SPaginationRequest
from schemas.projects import (
    SCreateProjectRequest, 
    SCreateProjectResponse, 
    SCreateTaskRequest, 
    SCreateTaskResponse, 
    SMyProjectsResponse
)
from services.projects import ProjectService
from services.roles import RoleService
from services.tasks import TaskService
from utils.enums.roles import CheckRoleStatus


verified_user = fastapi_users.current_user(verified=True, superuser=False) 

project_router = APIRouter(prefix="/project", tags=["projects"])


@project_router.get("/my")
async def my_projects(
    user: Annotated[UserORM, Depends(verified_user)],
    uow: ProjectUOWDep,
    role_id: RoleUUID = None,
    pagination: SPaginationRequest = Depends()
) -> SMyProjectsResponse:
    if (status:= await RoleService(uow).check_role(user, role_id)) != CheckRoleStatus.belong:
        raise HTTPException(status_code=422, detail=status.value)
    return await ProjectService(uow).get_project_by_creator_id(role_id, pagination)


@project_router.get("/{project_id}/select")
async def get_project_cookie(
    uow: ProjectUOWDep,
    project_id: UUID,
    role_id: RoleUUID = None,
    user: UserORM = Depends(verified_user)
) -> JSONResponse:
    if (status:= await RoleService(uow).check_role(user, role_id)) != CheckRoleStatus.belong:
        raise HTTPException(status_code=422, detail=status)
    return await ProjectService(uow).get_project_cookie(role_id, project_id)


@project_router.post("/new")
async def create_project(   
    user: Annotated[UserORM, Depends(verified_user)],
    uow: ProjectUOWDep,
    role_id: RoleUUID = None,
    request: SCreateProjectRequest = Depends()
) -> SCreateProjectResponse:
    if (status:= await RoleService(uow).check_role(user, role_id)) != CheckRoleStatus.belong:
        raise HTTPException(status_code=422, detail=status.value)
    response = await ProjectService(uow).create_project(role_id, request)
    id = response.id
    response = JSONResponse(content=response.model_dump(mode="json"))
    response.set_cookie("project_id", id)
    return response


@project_router.post("/add-task")
async def add_task(
    user: Annotated[UserORM, Depends(verified_user)],
    uow: ProjectUOWDep,
    request: Annotated[SCreateTaskRequest, Depends()],
    role_id: RoleUUID = None,
    project_id: ProjectUUID = None
) -> SCreateTaskResponse:
    if (status:= await RoleService(uow).check_role(user, role_id)) != CheckRoleStatus.belong:
        raise HTTPException(status_code=422, detail=status.value)
    if not (roles_list:= await TaskService(uow).can_send_task(role_id, request.responsobilities)):
        raise HTTPException(status_code=422, detail={
            "cannot send to": roles_list
        })
    response = await ProjectService(uow).add_task(role_id, request, project_id)
    return response
