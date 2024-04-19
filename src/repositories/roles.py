from typing import Type
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from database import BaseRepo
from logging import getLogger

from models import RoleORM
from models.structures import StructureORM

logger = getLogger(__name__)

class RoleRepo(BaseRepo):
    model = RoleORM


    async def get_for_info(self, id: UUID):
        return await self.get_with_options(
            id, 
            (
                joinedload(self.model.structure)
                .joinedload(StructureORM.org),
            )
        )
    

    async def get_for_page(self, id: UUID):
        return await self.get_with_options(
            id,
            (
                joinedload(self.model.structure)
                .joinedload(StructureORM.org),
                selectinload(self.model.subordinates),
                joinedload(self.model.rights)
             )
        )


    async def get_with_rights(self, id: UUID):
        return await self.get_with_options(
            id,
            (
                joinedload(self.model.rights),
            )
        )
