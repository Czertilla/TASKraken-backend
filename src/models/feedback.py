from enum import Enum
from typing import TYPE_CHECKING, Union
from uuid import UUID
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from utils.enums.feedback import Points


class FeedbackORM():
    __tablename__ = "feedbacks"

    task_id: Mapped[UUID|None] = mapped_column(ForeignKey("tasks.id", ondelete=""))
    report_id: Mapped[UUID|None] = mapped_column(ForeignKey("report.id", ondelete=""))
    mark: Mapped[Points]
    desctription: Mapped[str]
