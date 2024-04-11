from uuid import UUID

from models.files import FileORM
from database import BaseRepo


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
