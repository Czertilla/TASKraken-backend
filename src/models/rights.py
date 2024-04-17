from typing import TYPE_CHECKING
from uuid import UUID
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from utils.enums.abstract import AEnum
from utils.enums import TaskSendVector, RejectRight
from utils.mixins.sqlalchemy import TimestampMixin


if TYPE_CHECKING:
    from models.roles import RoleORM


class RoleRightORM(Base, TimestampMixin):
    __tablename__ = "rights"

    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))
    can_create_substructures: Mapped[bool] = mapped_column(default=False)
    can_create_subordinates: Mapped[bool] = mapped_column(default=False)
    can_send_task: Mapped[TaskSendVector] = mapped_column(default=TaskSendVector.__default__)
    can_send_report: Mapped[bool] = mapped_column(default=True)
    can_reject_task: Mapped[RejectRight] = mapped_column(default=RejectRight.__default__)


    role: Mapped["RoleORM"] = relationship(back_populates="rights")
