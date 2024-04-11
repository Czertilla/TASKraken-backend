from logging import getLogger
from uuid import UUID
from models.users import UserORM
from schemas.users import SSomeResponse
from utils.absract.service import BaseService

logger = getLogger(__name__)

class UserService(BaseService):
    async def check_username(self, value: str) -> bool:
        async with self.uow:
            self.uow.users.check_username(value)


    async def verify(self, id: UUID) -> UserORM|None:
        async with self.uow:
            user: UserORM = await self.uow.users.find_by_id(id)
            if user is None:
                logger.error("user %s not found", id)
                logger.warning("%s user not verified", id)
                return
            user.is_verified = True
            user.role = "specialist"
            await self.uow.users.merge(user)
            await self.uow.commit()
            return user
        
    async def get_some(self, user: UserORM) -> SSomeResponse:
        async with self.uow:
            user = await self.uow.users.find_by_id(user.id)
        return SSomeResponse(user.username)
            
    
