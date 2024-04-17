from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from database import BaseRepo
from logging import getLogger

from models import RoleORM

logger = getLogger(__name__)

class RoleRepo(BaseRepo):
    model = RoleORM


    async def get_for_info(self, id: UUID):
        return await self.get_with_options(
            id, 
            (joinedload(self.model.structure),)
        )
    
