from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import UUID
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from utils.mixins.advanced_orm import TaskProjectMixin


if TYPE_CHECKING:
    from models.checklists import ChecklistORM
    from models import StructureORM, RoleORM, FolderORM
    from models.report import ReportORM


class ProjectORM(TaskProjectMixin, Base):
    __tablename__ = "projects"

    organization_id: Mapped[UUID] = mapped_column(ForeignKey("structures.id"))

    organization: Mapped["StructureORM"] = relationship(back_populates="projects")
    creator: Mapped["RoleORM"] = relationship(back_populates="created_projects")

    tasks: Mapped[list["TaskORM"]] = relationship(back_populates="project")


class TaskORM(TaskProjectMixin, Base):
    __tablename__ = "tasks"

    level: Mapped[int] = mapped_column(default=0)
    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id"))
    head_task_id: Mapped[UUID|None] = mapped_column(ForeignKey("tasks.id"), nullable=True)
    folder_id: Mapped[UUID|None] = mapped_column(ForeignKey("folders.id"))

    head_task: Mapped[Optional["TaskORM"]] = relationship(back_populates="subtasks", remote_side="TaskORM.id")
    project: Mapped["ProjectORM"] = relationship(back_populates="tasks")
    creator: Mapped["RoleORM"] = relationship(back_populates="created_tasks")
    folder: Mapped["FolderORM"] = relationship(foreign_keys=[folder_id])

    subtasks: Mapped[list["TaskORM"]] = relationship(back_populates="head_task")
    responsibles: Mapped[list["RoleORM"]] = relationship(
        back_populates="tasks",
        secondary="responsibilities"
    )
    reports: Mapped[list["ReportORM"]] = relationship(back_populates="task")
    checklists: Mapped[list["ChecklistORM"]] = relationship(back_populates="task")
