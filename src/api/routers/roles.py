from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends

from api.auth.auth import fastapi_users
from api.dependencies import RoleUOWDep
from models.users import UserORM
from schemas.rights import SRoleRights
from services.roles import RoleService

get_verified = fastapi_users.current_user(verified=True, active=True)

roles = APIRouter(prefix="/role", tags=["roles"])

@roles.get("/{role_id}")
async def get_role_page(
    user: Annotated[UserORM, Depends(get_verified)],
    uow: RoleUOWDep,
    role_id: UUID
) -> SRoleInfo | SRolePage: # type: ignore
    return await RoleService(uow).get_role_page(user, role_id)


@roles.get("/{role_id}/check")
async def check_role(
    user: Annotated[UserORM, Depends(get_verified)],
    uow: RoleUOWDep,
    role_id: UUID
) -> SRoleCheckResponce: # type: ignore
    return await RoleService(uow).check_role(user, role_id)


@roles.get("/{role_id}/rights")
async def get_role_rights(
    user: Annotated[UserORM, Depends(get_verified)],
    uow: RoleUOWDep,
    role_id: UUID
) -> SRoleRights:
    return await RoleService(uow).get_role_rights(user, role_id)
