from uuid import UUID
from sqlalchemy import select
from database import BaseRepo
from logging import getLogger

from models import RoleORM

logger = getLogger(__name__)

class RoleRepo(BaseRepo):
    model = RoleORM
