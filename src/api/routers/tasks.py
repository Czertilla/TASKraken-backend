from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from api.auth.auth import fastapi_users
from api.dependencies import TaskUOWDep, RoleUUID, TaskUUID
from models.users import UserORM
from schemas.pagination import SPaginationRequest
from schemas.projects import  SMyProjectsResponse, SPutTaskRequest, STaskPage
from services.roles import RoleService
from services.tasks import TaskService
from utils.enums.roles import CheckRoleStatus


verified_user = fastapi_users.current_user(verified=True, superuser=False) 


task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.get("/my-assignments")
async def my_assignments(
    user: Annotated[UserORM, Depends(verified_user)],
    uow: TaskUOWDep,
    role_id: RoleUUID = None,
    pagination: SPaginationRequest = Depends()
) -> SMyProjectsResponse:
    if (status:= await RoleService(uow).check_role(user, role_id)) != CheckRoleStatus.belong:
        raise HTTPException(status_code=422, detail=status)
    return await TaskService(uow).get_tasks_by_creator_id(role_id, pagination)


@task_router.get("/my")
async def my_tasks(
    user: Annotated[UserORM, Depends(verified_user)],
    uow: TaskUOWDep,
    role_id: RoleUUID = None,
    pagination: SPaginationRequest = Depends()
) -> SMyProjectsResponse:
    if (status:= await RoleService(uow).check_role(user, role_id)) != CheckRoleStatus.belong:
        raise HTTPException(status_code=422, detail=status)
    return await TaskService(uow).get_tasks_by_responsobility_id(role_id, pagination)


@task_router.get("/{task_id}")
async def task_page(
    user: Annotated[UserORM, Depends(verified_user)],
    uow: TaskUOWDep,
    task_id: UUID,
    role_id: RoleUUID = None,
) -> STaskPage:
    if (status:= await RoleService(uow).check_role(user, role_id)) != CheckRoleStatus.belong:
        raise HTTPException(status_code=422, detail=status)
    content = await TaskService(uow).get_task_page(role_id, task_id)
    response = JSONResponse(content = content.model_dump(mode="json"))
    response.set_cookie(key="task_id", value=str(content.id))
    return response


# TODO solve problem with multirequests from different users
@task_router.put("/{task_id}")
async def edit_task(
    user: Annotated[UserORM, Depends(verified_user)],
    uow: TaskUOWDep,
    task: SPutTaskRequest,
    task_id: UUID,
    role_id: RoleUUID = None,
) -> STaskPage:
    if (status:= await RoleService(uow).check_role(user, role_id)) != CheckRoleStatus.belong:
        raise HTTPException(status_code=422, detail=status)
    content = await TaskService(uow).put_task(role_id, task)
    response = JSONResponse(content = content.model_dump(mode="json"))
    response.set_cookie(key="task_id", value=str(content.id))
    return response