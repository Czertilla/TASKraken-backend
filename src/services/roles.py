from logging import getLogger
from typing import Type
from uuid import UUID
from models.rights import RoleRightORM
from models.roles import RoleORM
from models.users import UserORM
from schemas.rights import RightsTemplateName, SRoleRights
from schemas.roles import SCreateVacancy, SGetRolePageRequest, SRoleCheckResponce, SRoleInfo, SRolePage
from utils.absract.service import BaseService
from utils.enums.rights import EditOtherRight
from utils.enums.roles import CheckRoleStatus, ViewMode


logger = getLogger(__name__)


class RoleService(BaseService):
    async def create_vacancy(self, data: SCreateVacancy):
        ...


    async def check_role(self, user: UserORM, role_id: UUID) -> CheckRoleStatus:
        async with self.uow:
            role = await self.uow.roles.get(role_id)
            if type(role) != RoleORM:
                return CheckRoleStatus.unexist
            if role.user_id == user.id:
                return CheckRoleStatus.belong
            else:
                return CheckRoleStatus.unbelonged
        return CheckRoleStatus.__default__


    def can_edit_rights(
        self, 
        target_role: RoleORM, 
        editor_role: RoleORM
    ) -> bool:
        match editor_role.rights.can_edit_other_rights:
            case EditOtherRight.organization:
                return (
                    target_role.structure.org_id ==
                    editor_role.structure.org_id 
                )
            case EditOtherRight.structure:
                return (
                    target_role.structure_id ==
                    editor_role.structure_id
                )
            case EditOtherRight.direct:
                return (
                    target_role.chief_id ==
                    editor_role.id
                )
            case _:
                return False
            
    
    async def get_role_rights(
        self,
        user: UserORM,
        request: SGetRolePageRequest
    )-> SRoleRights | SRoleCheckResponce:
        target_status = await self.check_role(user, request.target_id)
        flag = False
        if target_status == CheckRoleStatus.unbelonged:
            role_status = await self.check_role(user, request.role_id)
            if role_status == CheckRoleStatus.belong:
                target_role: RoleORM = await self.uow.roles.get_for_info(request.target_id)
                request_role: RoleORM = await self.uow.roles.get_for_info(request.role_id)
                if target_role is None or request_role is None:
                    return SRoleCheckResponce(status=CheckRoleStatus.error)
#TODO replace to can_view_role func
                if request_role.structure.org_id == target_role.structure.org_id:
                    flag = True
        elif target_status == CheckRoleStatus.belong:
            flag = True
        if flag:
            async with self.uow:
                rights: RoleRightORM = await self.uow.rights.get_by_role_id(request.target_id)
                data = dict(filter(
                    lambda x: x[0].startswith("can_"),
                    rights.__dict__.items()
                ))
            return SRoleRights(**data)
        return SRoleCheckResponce(status=target_status)
            


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
            view_mode = ViewMode.owner
            if status == CheckRoleStatus.unbelonged: 
                view_mode = ViewMode.info
                role: RoleORM = await self.uow.roles.get_for_info(request.target_id)
                if request.role_id is not None:
                    status = await self.check_role(user, request.role_id)
                    if status == CheckRoleStatus.belong:
                        watcher: RoleORM = await self.uow.roles.get_for_page(request.role_id)
                        if role.structure.org_id == watcher.structure.org_id:
                            if self.can_edit_rights(role, watcher):
                                view_mode = ViewMode.rights_patcher
#TODO add can_view_roles at elif
                            else:
                                view_mode = ViewMode.colleague
                        else:
                            status = CheckRoleStatus.unbelonged
            if status == CheckRoleStatus.belong:
                role: RoleORM = await self.uow.roles.get_for_page(request.target_id)
                if view_mode == ViewMode.owner and role.rights.can_edit_oneself_rights:
                    view_mode = ViewMode.owner_patcher
            data = {
                "view_mode": view_mode, 
                "user_id": role.user_id,
                "name": role.name,
                "org_id": role.structure.org_id,
                "org_name": role.structure.org.name,
                "level": role.level
            }
            if view_mode != ViewMode.info:
                data.update({
                    "struct_id": role.structure.id,
                    "chief_id": role.chief_id,
                    "subordinates_list": [sub.id for sub in role.subordinates],
                    "rights": role.rights
                })
                return SRolePage(**data)
            return SRoleInfo(**data)
