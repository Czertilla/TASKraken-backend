from typing import TYPE_CHECKING
from uuid import UUID
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from models.report import ReportORM



if TYPE_CHECKING:
    from models.users import UserORM
    from models.structures import StructureORM
    from models.tasks import ProjectORM, TaskORM
    from models.rights import RoleRightORM


class RoleORM(Base):
    __tablename__ = "roles"

    user_id: Mapped[UUID|None] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"))
    name: Mapped[str]
    level: Mapped[int] = mapped_column(default=0)
    structure_id: Mapped[UUID] = mapped_column(ForeignKey("structures.id", ondelete="CASCADE"))
    chief_id: Mapped[UUID|None] = mapped_column(ForeignKey("roles.id"), nullable=True)

    user: Mapped["UserORM"] = relationship(back_populates="roles")
    chief: Mapped["RoleORM"] = relationship(back_populates="subordinates", remote_side="RoleORM.id")
    structure: Mapped["StructureORM"] = relationship(back_populates="staff", foreign_keys=[structure_id])
    
    subordinates: Mapped[list["RoleORM"]] = relationship(back_populates="chief")
    created_projects: Mapped[list["ProjectORM"]] = relationship(back_populates="creator")
    created_tasks: Mapped[list["TaskORM"]] = relationship(back_populates="creator")
    tasks: Mapped[list["TaskORM"]] = relationship(
        back_populates="responsibles",
        secondary="responsibilities"
    )
    reports: Mapped[list["ReportORM"]] = relationship(back_populates="responsible")
