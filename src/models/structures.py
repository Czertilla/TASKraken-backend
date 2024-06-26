from typing import TYPE_CHECKING
from uuid import UUID
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from utils.mixins.sqlalchemy import TimestampMixin


if TYPE_CHECKING:
    from models.roles import RoleORM
    from models.tasks import ProjectORM


class StructureORM(Base, TimestampMixin):
    __tablename__ = "structures"

    head_id: Mapped[UUID|None] = mapped_column(ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str]
    desctription: Mapped[str] = mapped_column(default="")
    enclosure_id: Mapped[UUID|None] = mapped_column(ForeignKey("structures.id", ondelete="CASCADE"), nullable=True)
    org_id: Mapped[UUID|None] = mapped_column(ForeignKey("structures.id", ondelete="CASCADE"), nullable=True)

    enclosure: Mapped["StructureORM"] = relationship(
        back_populates="substructures", 
        remote_side="StructureORM.id",
        foreign_keys=enclosure_id)
    org: Mapped["StructureORM"] = relationship(foreign_keys=[org_id], backref="structures", remote_side="StructureORM.id")

    substructures: Mapped[list["StructureORM"]] = relationship(back_populates="enclosure", foreign_keys=enclosure_id)
    staff: Mapped[list["RoleORM"]] = relationship(back_populates="structure", foreign_keys="RoleORM.structure_id")
    projects: Mapped[list["ProjectORM"]] = relationship(back_populates="organization")
