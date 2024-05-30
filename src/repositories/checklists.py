from uuid import UUID

from sqlalchemy.ext.asyncio.session import AsyncSession

from models.checklists import ChecklistORM, CheckpointORM
from database import BaseRepo
from sqlalchemy.orm import selectinload



class CheckListRepo(BaseRepo):
    model = ChecklistORM
    
    class CheckPointRepo(BaseRepo):
        model = CheckpointORM

    def __init__(self, session: AsyncSession) -> None:
        self.checkpoints = self.CheckPointRepo(session)
        super().__init__(session)


    async def add_n_return(self, data: dict) -> model:
        points: list[dict] = data.pop("points")
        data.pop("id")
        checklist = await super().add_n_return(data)
        for point in points:
            point.update({"checklist_id": checklist.id})
            point.pop("id")
            await self.checkpoints.add_one(point)
        return checklist


    async def get_point(self, point_id, chlst_id) -> CheckPointRepo.model | None:
        point = await self.checkpoints.get(point_id)
        if isinstance(point, CheckpointORM):
            return point if point.checklist_id == chlst_id else None


    async def add_point(self, data: dict, chlst_id: UUID) -> None:
        if await self.get(chlst_id) is None:
            return
        data.update({"checklist_id": chlst_id})
        data.pop("id")
        await self.checkpoints.add_one(data)
