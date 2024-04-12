from uuid import UUID
from sqlalchemy import select
from database import BaseRepo
from logging import getLogger

from models.structures import StructureORM

logger = getLogger(__name__)

class StructureRepo(BaseRepo):
    model = StructureORM
