from typing import Annotated
import uuid

from fastapi_users import schemas
from pydantic import field_validator, validator
from fastapi import Depends

from repositories.users import UserRepo


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str
    role: str
    class Config:
        from_atributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str

class UserUpdate(schemas.BaseUserUpdate):
    pass