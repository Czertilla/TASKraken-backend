from typing import Annotated
from uuid import UUID
from fastapi import Depends, Query
from pydantic import BaseModel, Field

from schemas.rights import SRoleRights
from utils.enums.roles import CheckRoleStatus, ViewMode


class SCreateVacancy(BaseModel):
    name: Annotated[str, Query(max_length=64)]
    rights: Annotated[SRoleRights, Query(title='Vacancy rights')] = Depends()
    level: Annotated[int, Query(ge=0)]

    class Config:
        from_atributes = True


class SRoleCheckResponce(BaseModel):
    status = Annotated[CheckRoleStatus, Field()]

    class Config:
        from_atributes = True


class SGetRolePageRequest(BaseModel):
    role_id: UUID | None
    target_id: UUID


class SRoleInfo(BaseModel):
    view_mode: Annotated[ViewMode, Field()]
    
    user_id: UUID | None
    name: Annotated[str, Field(max_length=64)]
    org_name: Annotated[str, Field(max_length=512)]
    level: Annotated[int, Field(ge=0)]

    class Config:
        from_atributes = True


class SRolePage(SRoleInfo):
    struct_id: UUID
    org_id: UUID
    chief_id: UUID
    subordinates_list: list[UUID]
    rights: Annotated[SRoleRights, Field()]


