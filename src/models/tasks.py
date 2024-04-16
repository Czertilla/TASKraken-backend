from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import UUID
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import ForeignKey, func


if TYPE_CHECKING:
    from models.checklists import ChecklistORM
    from models import StructureORM, RoleORM, FolderORM
    from models.report import ReportORM

class TaskStatus(Enum):
    created = "created"
    frozen = "frozen"
    resumed = "resumed"
    closed = "closed"
    completed = "completed"

class TaskProjectMixin:
    @declared_attr
    def name(cls) ->  Mapped[str]:
        return mapped_column(nullable=False)
    
    @declared_attr
    def desctription(cls) -> Mapped[str]:
        return mapped_column(default="")
    
    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(default=func.now())
    
    @declared_attr
    def creator_id(cls) -> Mapped[UUID]:
        return mapped_column(ForeignKey("roles.id"))
    
    @declared_attr
    def edited_at(cls) -> Mapped[datetime|None]:
        return mapped_column(onupdate=func.now)
    
    @declared_attr
    def deadline(cls) -> Mapped[datetime|None]:
        return mapped_column(nullable=True)
    
    @declared_attr
    def status(cls) -> Mapped[TaskStatus]:
        return mapped_column(default=TaskStatus.created)
    
    @declared_attr
    def status_timestamp(cls) -> Mapped[datetime]:
        return mapped_column(default=func.now())


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
    head_task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), nullable=True)

    head_task: Mapped[Optional["TaskORM"]] = relationship(back_populates="subtasks", remote_side="TaskORM.id")
    project: Mapped["ProjectORM"] = relationship(back_populates="tasks")
    creator: Mapped["RoleORM"] = relationship(back_populates="created_tasks")
    # folder: Mapped["FolderORM"] = relationship(backref="enclosure", foreign_keys=[folder_id])

    subtasks: Mapped[list["TaskORM"]] = relationship(back_populates="head_task")
    responsibles: Mapped[list["RoleORM"]] = relationship(
        back_populates="tasks",
        secondary="responsibilities"
    )
    reports: Mapped[list["ReportORM"]] = relationship(back_populates="task")
    checklists: Mapped[list["ChecklistORM"]] = relationship(back_populates="task")
