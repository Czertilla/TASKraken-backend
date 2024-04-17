from .users import users_router
from .structures import structs_router
routers = (
    structs_router,
    users_router
)

from fastapi import FastAPI
from api.auth.routers import include_routers as include_auth_routers

def include_routers(app: FastAPI) -> None:
    for router in routers:
        app.include_router(router)
    include_auth_routers(app)

