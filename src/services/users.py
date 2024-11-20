from logging import getLogger
from uuid import UUID
from models.users import UserORM
from utils.absract.service import BaseService

logger = getLogger(__name__)

class UserService(BaseService):
    async def check_username(self, value: str) -> bool:
        async with self.uow:
            return (await self.uow.users.check_username(value))
