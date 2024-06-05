from api.auth.auth import fastapi_users, auth_backend
from api.auth.routers.verify import get_verify_router
from schemas.auth import UserCreate, UserRead, UserUpdate

from fastapi import FastAPI

def include_routers(app: FastAPI):
    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_users_router(
            UserRead, 
            UserUpdate, 
            requires_verification=True
        ),
        prefix="/users",
        tags=["users"],
    )

    app.include_router(
        fastapi_users.get_verify_router(UserRead),
        prefix="/auth",
        tags=["auth"]
    )

    app.include_router(
        get_verify_router(fastapi_users.get_user_manager, UserRead),
        prefix="/auth",
        tags=["auth"],
    )
