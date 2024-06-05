from datetime import datetime
from uuid import UUID
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import declared_attr, Mapped, mapped_column

from utils.enums import TaskStatus
from utils.mixins.sqlalchemy import TimestampMixin

class TaskProjectMixin(TimestampMixin):
    @declared_attr
    def name(cls) ->  Mapped[str]:
        return mapped_column(nullable=False)
    
    @declared_attr
    def desctription(cls) -> Mapped[str]:
        return mapped_column(default="")

    @declared_attr
    def creator_id(cls) -> Mapped[UUID]:
        return mapped_column(ForeignKey("roles.id"))
    
    @declared_attr
    def deadline(cls) -> Mapped[datetime|None]:
        return mapped_column(nullable=True)
    
    @declared_attr
    def status(cls) -> Mapped[TaskStatus]:
        return mapped_column(default=TaskStatus.__default__)
    
    @declared_attr
    def status_timestamp(cls) -> Mapped[datetime]:
        return mapped_column(default=func.now())

