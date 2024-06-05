from uuid import UUID

from models.files import FileORM, FolderORM
from database import BaseRepo
from sqlalchemy.orm import selectinload 


class FolderRepo(BaseRepo):
    model = FolderORM

    async def add_n_return(self, data: dict) -> model:
        return await super().add_n_return(data, (selectinload(self.model.files),))


class FileRepo(BaseRepo):
    model = FileORM
    async def upload_bytes(self, data: bytes) -> UUID:
        file_data = {
            "data": data
        }
        id = await self.add_one(file_data)
        return id


    async def download_bytes(self, file_id: UUID) -> bytes|None:
        file_orm: FileORM = await self.find_by_id(file_id)
        return file_orm.data
