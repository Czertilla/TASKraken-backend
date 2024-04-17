from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel, Field

from schemas.rights import SRoleRights
from utils.enums import RejectRight, TaskSendVector


class SCreateVacancy(BaseModel):
    name: Annotated[str, Query(max_length=25)]
    rights: Annotated[SRoleRights, Query(title='Vacancy rights')] = Depends()
    level: Annotated[int, Query(ge=0)]

    class Config:
        from_atributes = True
