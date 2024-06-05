from typing import Annotated, Optional, Union
from uuid import UUID
from fastapi import Depends, Query
from pydantic import BaseModel, Field

from schemas.pagination import SPaginationResponse
from schemas.rights import SHeadRights, SRoleRights
from utils.enums.roles import CheckRoleStatus, ViewMode


class SCreateSubordinate(BaseModel):
    name: Annotated[str, Query(max_length=64)]
    rights: Annotated[SRoleRights, Query(title='Vacancy rights')] = Depends()
    chief_id: Annotated[UUID|None, Query(default=None)] = None

    class Config:
        from_atributes = True


class SCreateStructHead(SCreateSubordinate):
    rights: Annotated[SHeadRights, Query(title='Vacancy rights')] = Depends()
    structure_id: UUID


class SRoleCheckResponce(BaseModel):
    request_key: str = None
    role_id: UUID = None
    status: Annotated[CheckRoleStatus, Field(default=CheckRoleStatus.__default__)]
    comment: str = None


    class Config:
        from_atributes = True


class SGetRolePageRequest(BaseModel):
    role_id: UUID | None = None
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
    chief_id: UUID | None
    subordinates_list: list[UUID]
    rights: Annotated[SRoleRights, Field()]


class SCreateRoleResponse(BaseModel):
    id: UUID
    name: str
    chief_id: UUID
    structure_id: UUID
    level: int
    rights: Annotated[SRoleRights, Field()]


class SRoleSelectResponse(BaseModel):
    id: UUID
    name: Annotated[str, Field(max_length=64)]
    level: int = None


class SRolePreview(SRoleSelectResponse):
    id: UUID
    name: Annotated[str, Field(max_length=64)]
    organization_name: str|None = None
    level: int = None


class SRoleSearchResponse(BaseModel):
    result: Annotated[list[SRolePreview], Field()]
    pagination: Annotated[SPaginationResponse, Field()] = None