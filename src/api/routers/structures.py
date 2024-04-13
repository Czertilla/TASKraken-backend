from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response

from api.auth.auth import fastapi_users
from api.dependencies import StructUOWDep
from models.users import UserORM
from schemas.structures import SRegistOrganization
from services.structures import StructureService

get_superuser = fastapi_users.current_user(verified=True, superuser=True) 

structs_router = APIRouter(prefix="/struct", tags=["structures"])

@structs_router.post()
async def regist_organization(
    user: Annotated[UserORM, Depends(get_superuser)],
    uow: StructUOWDep,
    organization_blank: SRegistOrganization = Depends()
):
    await StructureService(uow).regist_organization(user, organization_blank)
