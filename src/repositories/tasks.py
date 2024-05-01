from uuid import UUID
\
from database import BaseRepo
from models.tasks import TaskORM
from sqlalchemy.orm import selectinload

class TaskRepo(BaseRepo):
    model = TaskORM
    
    async def add_n_return(self, data: dict) -> model:
        return await super().add_n_return(
            data, 
            options=(
                selectinload(self.model.checklists),
                selectinload(self.model.responsibles)
            )
        )
    ...
