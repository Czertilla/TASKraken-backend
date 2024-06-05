from typing import Annotated, Optional, Union
from uuid import UUID
from fastapi import Depends, Query
from pydantic import BaseModel, Field

from utils.settings import getSettings


class SPaginationRequest(BaseModel):
    page: Annotated[Optional[int], Query(default=0, ge=0)]
    size: Annotated[Optional[int], Query(default=5, ge=1, le=getSettings().MAX_PAGE_SIZE)]
    
    class Config:
        from_atributes = True


class SPaginationResponse(SPaginationRequest):
    page: Annotated[int, Field(ge=0)]
    size: Annotated[int, Field(ge=1, le=getSettings().MAX_PAGE_SIZE)]
    total: Annotated[int, Field()]
