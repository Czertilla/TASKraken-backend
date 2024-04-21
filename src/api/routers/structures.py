from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends
from api.auth.auth import fastapi_users
from api.dependencies import StructUOWDep
from models.users import UserORM
from schemas.structures import SCreateStruct, SRegistOrganization, SRegistOrgResponse
from services.structures import StructureService


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
    role_id: UUID,
    request: SCreateStruct = Depends()
)-> SRegistOrgResponse:
    ...