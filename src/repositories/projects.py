from uuid import UUID

from sqlalchemy import select

from database import BaseRepo
from models.tasks import ProjectORM
from utils.enums.task import TaskStatus


class ProjectRepo(BaseRepo):
    model = ProjectORM
    
    async def get_status(self, id: UUID)-> TaskStatus:
        stmt = select(self.model.status).where(self.model.id==id)
        return (await self.execute(stmt)).scalar_one_or_none()
    ...
