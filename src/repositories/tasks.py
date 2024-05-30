from uuid import UUID
\
from database import BaseRepo
from models.tasks import TaskORM
from sqlalchemy.orm import selectinload, joinedload

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
    

    async def get_for_page(self, task_id: UUID) -> model:
        return await self.get_with_options(
            id=task_id,
            options=(
                selectinload(self.model.responsibles),
                selectinload(self.model.subtasks),
                joinedload(self.model.project),
                joinedload(self.model.head_task)
            )
        )