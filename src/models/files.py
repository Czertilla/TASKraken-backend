from sqlalchemy import func
from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class FileORM(Base):
    __tablename__ = "files"

    data: Mapped[bytes]
    created: Mapped[datetime] = mapped_column(default=func.now())
    changed: Mapped[datetime|None]
