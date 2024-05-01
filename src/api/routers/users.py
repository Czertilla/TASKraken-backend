from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response

from api.auth.auth import fastapi_users
from api.dependencies import UsersUOWDep
from models.users import UserORM
from schemas.projects import SCreateProjectRequest, SCreateTaskRequest
from services.users import UserService

verified_user = fastapi_users.current_user(verified=True, superuser=False) 

users_router = APIRouter(prefix="/user", tags=["user"])

@users_router.get("/")
async def get_some(
    user: Annotated[UserORM, Depends(verified_user)],
    uow: UsersUOWDep,
    request: SCreateTaskRequest = Depends()
    ):
    response = await UserService(uow).get_some(user)
    if response is None:
        raise HTTPException(status_code=404, detail="Case with appropriate skill value not found")
    return Response(content=response.photo, media_type="image/png")
