from typing import TYPE_CHECKING
from uuid import UUID
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func

if TYPE_CHECKING:
    from models import TaskORM
    from models.roles import RoleORM
    from models.files import FolderORM


class ReportORM(Base):
    __tablename__ = "reports"

    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    responsible_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id", ondelete="SET NULL"))
    folder_id: Mapped[UUID|None] = mapped_column(ForeignKey("folders.id"))
    
    # folder: Mapped["FolderORM"] = relationship(back_populates="enclosure", foreign_keys=[folder_id])
    responsible: Mapped["RoleORM"] = relationship(back_populates="reports")
    task: Mapped["TaskORM"] = relationship(back_populates="reports")


