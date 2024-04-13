
from datetime import datetime
from typing import Annotated
from fastapi import Query
from pydantic import BaseModel, Field


class SRegistOrganization(BaseModel):
    name: Annotated[str, Query(max_length="50")]
    desctription: Annotated[str, Query(max_length="500")]

    class Config:
        from_atributes = True
