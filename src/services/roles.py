from logging import getLogger
from uuid import UUID
from models.rights import RoleRightORM
from models.roles import RoleORM
from models.users import UserORM
from schemas.rights import RightsTemplateName
from schemas.roles import SCreateVacancy
from utils.absract.service import BaseService

logger = getLogger(__name__)

class RoleService(BaseService):
    async def create_vacancy(self, data: SCreateVacancy):
        ...
