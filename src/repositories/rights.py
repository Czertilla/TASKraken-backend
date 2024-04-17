from database import BaseRepo
from logging import getLogger

from models.rights import RoleRightORM

logger = getLogger(__name__)

class RightRepo(BaseRepo):
    model = RoleRightORM
