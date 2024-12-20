from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Cookie, Depends, Request
from fastapi.responses import JSONResponse
from fastapi_filter import FilterDepends

from api.auth.auth import fastapi_users
from api.dependencies import RoleUOWDep, RoleUUID, StructUOWDep
from schemas.filters.roles import RoleFilter
from models.users import UserORM
from schemas.pagination import SPaginationRequest
from schemas.rights import SRoleRights
from schemas.roles import SCreateRoleResponse, SCreateStructHead, SCreateSubordinate, SGetRolePageRequest, SRoleCheckResponce, SRoleInfo, SRolePage, SRoleSearchResponse
from services.roles import RoleService

get_verified = fastapi_users.current_user(verified=True, active=True)
get_optional = fastapi_users.current_user(optional=True)

roles = APIRouter(prefix="/role", tags=["roles"])


@roles.get("/search")
async def search_roles(
    uow: RoleUOWDep,
    user: UserORM = Depends(get_optional),
    filters: RoleFilter = FilterDepends(RoleFilter),
    pagination: SPaginationRequest = Depends()
) -> SRoleSearchResponse:
    return await RoleService(uow).search(filters, pagination)

@roles.get("/my-roles")
async def my_roles(
    uow: RoleUOWDep,
    user: UserORM = Depends(get_verified),
    pagination: SPaginationRequest = Depends()
) -> SRoleSearchResponse:
    return await RoleService(uow).search(RoleFilter(user_id=user.id), pagination)


@roles.get("/{role_id}/select")
async def select_role(
    uow: RoleUOWDep,
    role_id: UUID,
    user: UserORM = Depends(get_verified)
) -> JSONResponse:
    return await RoleService(uow).get_role_cookie(user, role_id)


@roles.get("/{target_id}")
async def get_role_page(
    user: Annotated[UserORM, Depends(get_optional)],
    uow: RoleUOWDep,
    request: Annotated[SGetRolePageRequest, Depends()]
) -> SRoleInfo | SRolePage:
    return await RoleService(uow).get_role_page(user, request)


@roles.get("/{target_id}/check")
async def check_role(
    user: Annotated[UserORM, Depends(get_verified)],
    uow: RoleUOWDep,
    target_id: UUID
) -> SRoleCheckResponce:
    return SRoleCheckResponce(status=await RoleService(uow).check_role(user, target_id))


@roles.get("/{target_id}/rights")
async def get_role_rights(
    user: Annotated[UserORM, Depends(get_verified)],
    uow: RoleUOWDep,
    request: Annotated[SGetRolePageRequest, Depends()]
) -> SRoleRights:
    return await RoleService(uow).get_role_rights(user, request)


@roles.post("/create")
async def create_subordinate(
    user: Annotated[UserORM, Depends(get_verified)],
    uow: RoleUOWDep,
    role_id: RoleUUID = None,
    request: SCreateSubordinate = Depends()
) -> SCreateRoleResponse:
    return await RoleService(uow).create_subordinate(user, role_id, request)


@roles.post("/create_struct_head")
async def create_struct_head(
    user: Annotated[UserORM, Depends(get_verified)],
    uow: StructUOWDep,
    role_id: RoleUUID = None,
    request: SCreateStructHead = Depends()
) -> SCreateRoleResponse:
    return await RoleService(uow).create_subordinate(user, role_id, request)
