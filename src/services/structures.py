from logging import getLogger
from uuid import UUID
from models.roles import RoleORM
from models.structures import StructureORM
from models.users import UserORM
from schemas.roles import SRoleRights
from schemas.structures import SCreateStruct, SCreateStructResponse, SRegistOrgResponse, SRegistOrganization
from utils.absract.service import BaseService
from utils.enums.rights import CreateStructRight

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
            org: StructureORM = await self.uow.structs.add_n_return(org_data)
            gen_dir_data.update({
                "structure_id": org.id
            })
            org.org_id = org.id
            head_id = await self.uow.roles.add_one(gen_dir_data)
            org.head_id = head_id
            await self.uow.rights.add_one({
                "role_id": head_id,
                **rights_data
            })
            await self.uow.commit(True)
        return SRegistOrgResponse(
            gen_dir_id=head_id,
            org_id=org.id
        )
    

    def can_create_structs(
        self, 
        role: RoleORM,
        enclosure: StructureORM
    )-> bool:
        match role.rights.can_create_substructures:
            case CreateStructRight.in_organization:
                return (
                    role.structure.org_id ==
                    enclosure.org_id
                )
            case CreateStructRight.in_overstruct:
#TODO realize
                return (
                    False
                )
            case CreateStructRight.in_struct:
                return (
                    role.structure_id ==
                    enclosure.id
                )
            case _:
                return False

    async def create_substruct(self, role_id: UUID, data: SCreateStruct) -> SCreateStructResponse:
        async with self.uow:
            role: RoleORM = await self.uow.roles.get_for_rights_check(role_id)
            if role is None:
                return SCreateStructResponse(reject_message="role unexist")
            enclosure: StructureORM = await self.uow.structs.get(data.enclosure_id)
            if enclosure is None:
                return SCreateStructResponse(reject_message="enclosure unexist")
            await self.uow.commit(flush=True)
            if not self.can_create_structs(role, enclosure):
                return SCreateStructResponse(reject_message="creating forbidden")
            data: dict = data.model_dump()
            data.update({
                "org_id": 
                    enclosure.id
                    if enclosure.org_id is None and enclosure.enclosure_id is None 
                    else enclosure.org_id
            })
            struct_id: UUID = await self.uow.structs.add_one(data)
            await self.uow.commit()
            data.update({"id": struct_id})
        return SCreateStructResponse(**data)
