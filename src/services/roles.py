from logging import getLogger
from typing import Type
from uuid import UUID
from models.rights import RoleRightORM
from models.roles import RoleORM
from models.structures import StructureORM
from models.users import UserORM
from schemas.rights import RightsTemplateName, SRoleRights
from schemas.roles import (
    SCreateRoleResponse,
    SCreateStructHead, 
    SCreateSubordinate, 
    SGetRolePageRequest, 
    SRoleCheckResponce, 
    SRoleInfo, 
    SRolePage
)
from utils.absract.service import BaseService
from utils.enums.rights import CreateVacancyRigth, EditOtherRight
from utils.enums.roles import CheckRoleStatus, ViewMode


logger = getLogger(__name__)


class RoleService(BaseService):
    async def create_subordinate(
        self, 
        user: UserORM, 
        role_id: UUID, 
        data: SCreateSubordinate | SCreateStructHead
    ) -> SCreateRoleResponse | SRoleCheckResponce:
        status = await self.check_role(user, role_id)
        if status != CheckRoleStatus.belong:
            return SRoleCheckResponce(
                status=status,
                request_key="role_id",
                role_id=role_id
            )
        async with self.uow:
            chief_role: RoleORM = await self.uow.roles.get(data.chief_id)
            if chief_role is None:
                return SRoleCheckResponce(
                    status=CheckRoleStatus.unexist,
                    request_key="chief_id",
                    role_id=data.chief_id
                )
            creator_role: RoleORM = await self.uow.roles.get_for_page(role_id)
            if not (await self.can_create_roles(creator_role, chief_role)):
                return SRoleCheckResponce(
                    status=CheckRoleStatus.forbidden,
                    request_key="role_id",
                    role_id=role_id
                )
            level = chief_role.level + 1
            if type(data) == SCreateStructHead:
                struct: StructureORM = self.uow.structs.get(struct_id:=data.structure_id)
                if struct is None:
                    return SRoleCheckResponce(
                        status=CheckRoleStatus.unexist,
                        role_id=struct_id,
                        request_key="struct_id"
                    )
                if struct.head_id is not None:
                    return SRoleCheckResponce(
                        status=CheckRoleStatus.error,
                        role_id=struct_id,
                        request_key="struct_id",
                        comment=f"struct head already exist: {struct.head_id}"
                    )
                if struct.enclosure_id != chief_role.structure_id:
                    return SRoleCheckResponce(
                        status=CheckRoleStatus.unbelonged,
                        role_id=struct_id,
                        request_key="struct_id",
                        comment="chief must be staff of oversturct"
                    )
            else:
                struct_id = chief_role.structure_id
        data: dict = data.model_dump()
        data.update({
            "level": level,
            "structure_id": struct_id
        })
        return await self.create_role(data)

    
    async def create_role(self, role_data: dict):
        rights: dict = role_data.pop("rights", {})
        template_name = rights.pop("template", RightsTemplateName.null)
        async with self.uow:
            id: UUID|None = await self.uow.roles.add_one(role_data)
            rights.update({"role_id": id})
            await self.uow.rights.add_one(rights)
            await self.uow.commit()
        if id is None:
            return SRoleCheckResponce(
                status=CheckRoleStatus.error,
                comment="database error"
            )
        else:
            role_data.update({"id": id})
            return SCreateRoleResponse(
                **role_data,
                rights=rights
            )


    async def check_role(self, user: UserORM, role_id: UUID) -> CheckRoleStatus:
        if type(user) != UserORM:
            return CheckRoleStatus.unbelonged
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
                ) if target_role.chief_id is not None else False
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
            
    
    async def can_create_roles(
        self,
        creator_role: RoleORM,
        chief_role: RoleORM
    ) -> bool:
        async with self.uow:
            match creator_role.rights.can_create_subordinates:
                case CreateVacancyRigth.organization:
                    return(
                        creator_role.structure.org_id ==
                        chief_role.structure.org_id
                    )
                case CreateVacancyRigth.in_overstructure:
#TODO change to realization for overstruct
                    return(
                        creator_role.structure.org_id ==
                        chief_role.structure.org_id
                    )
                case CreateVacancyRigth.lower_level:
                    return(
                        creator_role.level >=
                        chief_role.level
                    )
                case CreateVacancyRigth.subordinates:
                    return(
                        creator_role.id == chief_role.id
                    )
                case CreateVacancyRigth.downstream:
                    if creator_role.level < chief_role:
                        return False
#TODO need test is_on_downstrem
                    return await self.uow.roles.is_on_downstream(
                        creator_role.id,
                        chief_role.id,
                    ) if creator_role.id != chief_role.id else True
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
        return SRoleCheckResponce(
            status=target_status,
            request_key="target_id",
            role_id=request.target_id
        )
            

    async def get_role_page(
        self, 
        user: UserORM|None, 
        request: SGetRolePageRequest
    ) -> SRoleInfo | SRolePage | SRoleCheckResponce:
        status = await self.check_role(user, request.target_id)
        if status == CheckRoleStatus.unexist:
            return SRoleCheckResponce(
                status=status.value,
                request_key="target_id",
                role_id=request.target_id
            )
        async with self.uow:
            data = {}
            view_mode = ViewMode.owner
            if status == CheckRoleStatus.unbelonged or user is None: 
                view_mode = ViewMode.info
                role: RoleORM = await self.uow.roles.get_for_info(request.target_id)
                if request.role_id is not None and user is not None:
                    status = await self.check_role(user, request.role_id)
                    if status == CheckRoleStatus.belong and user.is_verified:
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
