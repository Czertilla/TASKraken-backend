from typing import TYPE_CHECKING
from uuid import UUID
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from models.roles import RoleORM
    from models.tasks import ProjectORM

class StructureORM(Base):
    __tablename__ = "structures"

    head_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"))
    name: Mapped[str]
    desctription: Mapped[str] = mapped_column(default="")
    enclosure_id: Mapped[UUID|None] = mapped_column(ForeignKey("structures.id", ondelete="CASCADE"), nullable=True)

    enclosure: Mapped["StructureORM"] = relationship(back_populates="substructures")

    substructures: Mapped[list["StructureORM"]] = relationship(back_populates="enclosure")
    staff: Mapped[list["RoleORM"]] = relationship(back_populates="structure")
    projects: Mapped[list["ProjectORM"]] = relationship(back_populates="organization")