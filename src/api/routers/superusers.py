from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response

from api.auth.auth import fastapi_users
from api.dependencies import StructUOWDep
from models.users import UserORM
from schemas.structures import SRegistOrganization
from services.structures import StructureService

get_super_user = fastapi_users.current_user(superuser=True, verified=True)

sups = APIRouter(prefix="/sups", tags=["superuser"])
