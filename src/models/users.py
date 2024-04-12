from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from models.files import FolderORM

if TYPE_CHECKING:
    from models.roles import RoleORM



class UserORM(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(unique=True)
    photo_folder_id: Mapped[UUID] = mapped_column(ForeignKey("folders.id"), default=FolderORM)

    roles: Mapped[list["RoleORM"]] = relationship(back_populates="user")
