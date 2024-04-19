from uuid import UUID

from sqlalchemy import select
from database import BaseRepo
from logging import getLogger

from models.rights import RoleRightORM

logger = getLogger(__name__)

class RightRepo(BaseRepo):
    model = RoleRightORM


    async def get_by_role_id(self, role_id: UUID) -> model|None:
        stmt = (
            select(self.model)
            .where(self.model.role_id==role_id)
        )
        return (await self.execute(stmt)).scalar_one_or_none()
