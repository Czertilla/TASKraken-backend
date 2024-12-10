import asyncio
from fastapi import APIRouter

from api.auth.auth import fastapi_users
from api.dependencies import UsersUOWDep
from schemas.users import SCheckResponse
from services.users import UserService

verified_user = fastapi_users.current_user(verified=True, superuser=False) 

users_router = APIRouter(prefix="/user", tags=["user"])

@users_router.get("/check/{username}")
async def check_username(
    uow: UsersUOWDep,
    username: str
) -> SCheckResponse:
    await asyncio.sleep(0.2)
    return SCheckResponse(
        username=username, 
        exists=(await UserService(uow).check_username(username))
    )
