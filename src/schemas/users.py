
from datetime import datetime
from typing import Annotated
from fastapi import Query
from pydantic import BaseModel, Field


class SSomeResponse(BaseModel):
    username: Annotated[str, Field(max_length=50)]

    class Config:
        from_atributes = True
