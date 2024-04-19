from typing import Annotated
from fastapi import APIRouter, Depends
from api.auth.auth import fastapi_users
from api.dependencies import StructUOWDep
from models.users import UserORM
from schemas.structures import SRegistOrganization, SRegistOrgResponse
from services.structures import StructureService


get_verified_user = fastapi_users.current_user(verified=True, active=True) 
get_super_user = fastapi_users.current_user(superuser=True, active=True)


structs_router = APIRouter(prefix="/struct", tags=["structures"])


@structs_router.post("/regist")
async def regist_organization(
    user: Annotated[UserORM, Depends(get_verified_user)],
    uow: StructUOWDep,
    organization_blank: SRegistOrganization = Depends()
)-> SRegistOrgResponse:
    return await StructureService(uow).regist_organization(user, organization_blank)
