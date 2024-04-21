from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends

from api.auth.auth import fastapi_users
from api.dependencies import RoleUOWDep
from models.users import UserORM
from schemas.rights import SRoleRights
from schemas.roles import SCreateRoleResponse, SCreateSubordinate, SGetRolePageRequest, SRoleCheckResponce, SRoleInfo, SRolePage
from services.roles import RoleService

get_verified = fastapi_users.current_user(verified=True, active=True)

roles = APIRouter(prefix="/role", tags=["roles"])

@roles.get("/{target_id}")
async def get_role_page(
    user: Annotated[UserORM, Depends(get_verified)],
    uow: RoleUOWDep,
    request: Annotated[SGetRolePageRequest, Depends()]
) -> SRoleInfo | SRolePage | SRoleCheckResponce:
    return await RoleService(uow).get_role_page(user, request)


@roles.get("/{role_id}/check")
async def check_role(
    user: Annotated[UserORM, Depends(get_verified)],
    uow: RoleUOWDep,
    role_id: UUID
) -> SRoleCheckResponce:
    return SRoleCheckResponce(status=await RoleService(uow).check_role(user, role_id))


@roles.get("/{target_id}/rights")
async def get_role_rights(
    user: Annotated[UserORM, Depends(get_verified)],
    uow: RoleUOWDep,
    request: Annotated[SGetRolePageRequest, Depends()]
) -> SRoleRights | SRoleCheckResponce:
    return await RoleService(uow).get_role_rights(user, request)


@roles.post("/create")
async def create_subordinate(
    user: Annotated[UserORM, Depends(get_verified)],
    uow: RoleUOWDep,
    role_id: UUID,
    request: SCreateSubordinate = Depends()
) -> SCreateRoleResponse | SRoleCheckResponce:
    return await RoleService(uow).create_subordinate(user, role_id, request)
