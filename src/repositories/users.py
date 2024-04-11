from typing import AsyncGenerator
from uuid import UUID
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import Depends
from database import new_session, BaseRepo
from logging import getLogger

from models.users import UserORM

logger = getLogger(__name__)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, UserORM)

class UserRepo(BaseRepo):
    model = UserORM

    async def check_username(self, value) -> bool:
        user = (
            await self.execute(
                select(UserORM).
                where(UserORM.username == value)
            )
        ).scalar_one_or_none()
        return user is not None

    async def verify(self, id: UUID) -> UserORM|None:
        user = await self.find_by_id(id)
        if user is None:
            logger.error("user %s not found", id)
            logger.warning("%s user not verified", id)
            return
        user.is_verified = True
        user.role = "specialist"
        await self.merge(user)
        return user
    
    async def set_manager(self, id: UUID):
        user = await self.find_by_id(id)
        if user is None:
            logger.error("user %s not found", id)
            logger.warning("superuser status for user %s is not set", id)
            return
        user.is_superuser = True
        user.is_active = True
        user.is_verified = True
        user.role = "manager"
        await self.merge(user)


