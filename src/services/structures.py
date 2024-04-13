from logging import getLogger
from uuid import UUID
from models.structures import StructureORM
from models.users import UserORM
from schemas.structures import SRegistOrganization
from utils.absract.service import BaseService

logger = getLogger(__name__)

class StructureService(BaseService):
    async def regist_organization(self, founder: UserORM, org_data: SRegistOrganization):
        (org_data := org_data.model_dump()).update({
            "head_id": founder.id
        })
        async with self.uow:
            await self.uow.structs.add_one(org_data)
            await self.uow.commit()

