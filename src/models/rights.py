from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from database import Base
from utils.enums import SendTaskVector, RejectTaskRight
from utils.enums.rights import CreateStructRight, CreateVacancyRigth, EditOtherRight, SendPetitionVector
from utils.mixins.sqlalchemy import TimestampMixin


if TYPE_CHECKING:
    from models.roles import RoleORM


class RoleRightORM(Base, TimestampMixin):
    __tablename__ = "rights"

    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))
    template_id: Mapped[UUID|None] = mapped_column(ForeignKey("rights.id", ondelete="SET NULL"), nullable=True)
    can_create_substructures: Mapped[CreateStructRight] = mapped_column(default=CreateStructRight.__default__)
    can_create_subordinates: Mapped[CreateVacancyRigth] = mapped_column(default=CreateVacancyRigth.__default__)
    can_create_project: Mapped[bool] = mapped_column(default=False)
    can_send_task: Mapped[SendTaskVector] = mapped_column(default=SendTaskVector.__default__)
    can_send_report: Mapped[bool] = mapped_column(default=True)
    can_send_petition: Mapped[SendPetitionVector] = mapped_column(default=SendPetitionVector.__default__)
    can_reject_task: Mapped[RejectTaskRight] = mapped_column(default=RejectTaskRight.__default__)
#TODO add column 'can_view_roles' with type 'ViewRoleRight'
    can_edit_other_rights: Mapped[EditOtherRight] = mapped_column(default=EditOtherRight.__default__)
    can_edit_oneself_rights: Mapped[bool] = mapped_column(default=False)

    role: Mapped["RoleORM"] = relationship(back_populates="rights")
