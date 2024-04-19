from logging import getLogger
from uuid import UUID
from models.roles import RoleORM
from models.structures import StructureORM
from models.users import UserORM
from schemas.roles import SRoleRights
from schemas.structures import SRegistOrgResponse, SRegistOrganization
from utils.absract.service import BaseService

logger = getLogger(__name__)

class StructureService(BaseService):
    async def regist_organization(self, user: UserORM, org_data: SRegistOrganization)-> SRegistOrgResponse:
        async with self.uow:
            org_data: dict = org_data.model_dump()
            rights_data: dict = org_data.pop("rights")
            template = rights_data.pop("template")
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
            head_id = await self.uow.roles.add_one(gen_dir_data)
            org.head_id = head_id
            org.org_id = org.id
            await self.uow.rights.add_one({
                "role_id": head_id,
                **rights_data
            })
            await self.uow.commit(True)
        return SRegistOrgResponse(
            gen_dir_id=head_id,
            org_id=structure_id
        )

