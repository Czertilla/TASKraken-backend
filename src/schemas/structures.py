
from datetime import datetime
from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel, Field

from schemas.rights import SGenDirRights


class SRegistOrganization(BaseModel):
    name: Annotated[str, Query(max_length=64)]
    desctription: Annotated[str, Query(max_length=512)]
    gen_dir_name: Annotated[str, Query(max_length=64)]
    rights: Annotated[SGenDirRights, Query(title="Gen-Dir Rights")] = Depends()

    class Config:
        from_atributes = True
