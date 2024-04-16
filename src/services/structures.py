from logging import getLogger
from uuid import UUID
from models.roles import RoleORM
from models.structures import StructureORM
from models.users import UserORM
from schemas.structures import SRegistOrganization
from utils.absract.service import BaseService

logger = getLogger(__name__)

class StructureService(BaseService):
    async def regist_organization(self, user: UserORM, org_data: SRegistOrganization):
        async with self.uow:
            org_data: dict = org_data.model_dump()
            gen_dir_data: dict = {
                "name": org_data.pop("gen_dir_name"),
                "user_id": user.id
            }
            org: StructureORM = await self.uow.structs.get(
                structure_id:= await self.uow.structs.add_one(org_data)
            )
            gen_dir_data.update({
                "structure_id": structure_id
            })
            org.head_id = await self.uow.roles.add_one(gen_dir_data)
            await self.uow.commit(True)

