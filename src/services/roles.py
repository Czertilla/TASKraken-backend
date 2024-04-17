from logging import getLogger
from typing import Type
from uuid import UUID
from models.rights import RoleRightORM
from models.roles import RoleORM
from models.users import UserORM
from schemas.rights import RightsTemplateName
from schemas.roles import SCreateVacancy, SGetRolePageRequest, SRoleCheckResponce, SRoleInfo, SRolePage
from utils.absract.service import BaseService
from utils.enums.roles import CheckRoleStatus


logger = getLogger(__name__)


class RoleService(BaseService):
    async def create_vacancy(self, data: SCreateVacancy):
        ...


    async def check_role(self, user: UserORM, role_id: UUID) -> SRoleCheckResponce:
        async with self.uow:
            role = await self.uow.roles.get(role_id)
            if type(role) != RoleORM:
                return CheckRoleStatus.unexist
            if role.user_id == user.id:
                return CheckRoleStatus.belong
        return CheckRoleStatus.__default__


    async def get_role_page(
        self, 
        user: UserORM, 
        request: SGetRolePageRequest
    ) -> SRoleInfo | SRolePage | SRoleCheckResponce:
        status = await self.check_role(user, request.target_id)
        if status == CheckRoleStatus.unexist:
            return SRoleCheckResponce(status=status)
        async with self.uow:
            data = {}
            flag = False
            if status == CheckRoleStatus.unbelonged:
                role: RoleORM = await self.uow.roles.get_for_info(request.target_id)
            elif status == CheckRoleStatus.belong:
                role: RoleORM = await self.uow.roles.get_for_page(request.target_id)
                flag = True
            data = {
                "user_id": role.user_id,
                "name": role.name,
                "org_name": role.structure.org.name,
                "level": role.level
            }
            if flag:
                data.update({
                    "struct_id": role.structure.id,
                    "org_id": role.structure.org_id,
                    "chief_id": role.chief_id,
                    "subordinates_list": [sub.id for sub in role.subordinates],
                    "rights": role.rights
                })
            return data
