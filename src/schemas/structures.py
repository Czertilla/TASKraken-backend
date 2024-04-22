
from datetime import datetime
from typing import Annotated, ClassVar
from uuid import UUID
from fastapi import Depends, Query
from pydantic import BaseModel, Field

from schemas.rights import SGenDirRights


class SCreateStruct(BaseModel):
    name: Annotated[str, Query(max_length=64)]
    desctription: Annotated[str, Query(max_length=512)]
    enclosure_id: Annotated[UUID, Query(title="id of overstruct")]

    class Config:
        from_atributes = True


class SRegistOrganization(SCreateStruct):
    gen_dir_name: Annotated[str, Query(max_length=64)]
    rights: Annotated[SGenDirRights, Query(title="Gen-Dir Rights")] = Depends()
    enclosure_id: ClassVar[None]


class SRegistOrgResponse(BaseModel):
    gen_dir_id: Annotated[UUID, Field()]
    org_id: Annotated[UUID, Field()]


class SCreateStructResponse(SCreateStruct):
    id: UUID | None = None
    reject_message: str = None
