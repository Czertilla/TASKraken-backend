from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from api.auth.auth import fastapi_users
from api.dependencies import RoleUUID, StructUOWDep
from models.users import UserORM
from schemas.structures import SCreateStruct, SCreateStructResponse, SRegistOrganization, SRegistOrgResponse
from services.roles import RoleService
from services.structures import StructureService
from utils.enums.roles import CheckRoleStatus


get_verified = fastapi_users.current_user(verified=True, active=True) 
get_super = fastapi_users.current_user(superuser=True, active=True)


structs_router = APIRouter(prefix="/struct", tags=["structures"])


@structs_router.post("/regist")
async def regist_organization(
    user: Annotated[UserORM, Depends(get_verified)],
    uow: StructUOWDep,
    organization_blank: SRegistOrganization = Depends()
)-> SRegistOrgResponse:
    return await StructureService(uow).regist_organization(user, organization_blank)


@structs_router.post("/create")
async def create_substruct(
    user: Annotated[UserORM, Depends(get_verified)],
    uow: StructUOWDep,
    role_id: RoleUUID = None,
    request: SCreateStruct = Depends()
)-> SCreateStructResponse:
    if (status:=await RoleService(uow).check_role(user, role_id)) != CheckRoleStatus.belong:
        raise HTTPException(status_code=403, detail=status)
    response = await StructureService(uow).create_substruct(role_id, request)
    if response.reject_message is not None:
        raise HTTPException(status_code=403, detail=response.reject_message)
    return response
    