from typing import TYPE_CHECKING
from uuid import UUID
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from models.tasks import TaskORM


class ChecklistORM(Base):
    __tablename__ = "checklists"

    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    name: Mapped[str]

    task: Mapped["TaskORM"] = relationship(back_populates="checklists")

    checkpoints: Mapped[list["CheckpointORM"]] = relationship(back_populates="checklist")


class CheckpointORM(Base):
    __tablename__ = "checkpoints"

    checklist_id: Mapped[UUID] = mapped_column(ForeignKey("checklists.id", ondelete="CASCADE"))
    name: Mapped[str]
    done: Mapped[bool] = mapped_column(default=False)

    checklist: Mapped["ChecklistORM"] = relationship(back_populates="checkpoints")

