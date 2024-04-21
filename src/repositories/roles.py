from typing import Type
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from database import BaseRepo
from logging import getLogger

from models import RoleORM
from models.structures import StructureORM
from utils.enums.roles import DownstreamStatus

logger = getLogger(__name__)

class RoleRepo(BaseRepo):
    model = RoleORM


    async def get_for_info(self, id: UUID):
        return await self.get_with_options(
            id, 
            (
                joinedload(self.model.structure)
                .joinedload(StructureORM.org),
            )
        )
    

    async def get_for_page(self, id: UUID):
        return await self.get_with_options(
            id,
            (
                joinedload(self.model.structure)
                .joinedload(StructureORM.org),
                selectinload(self.model.subordinates),
                joinedload(self.model.rights)
             )
        )


    async def get_with_rights(self, id: UUID):
        return await self.get_with_options(
            id,
            (
                joinedload(self.model.rights),
            )
        )
    

    async def get_for_rights_check(self, id: UUID):
        return await self.get_with_options(
            id, 
            (
                joinedload(self.model.rights),
                joinedload(self.model.structure)
            )
        )
    

    async def is_on_downstream(
        self, 
        first_id: UUID, 
        second_id: UUID,
        reverse_possible: bool = False,
        /,
        first_call: bool = True,
        first_level: int = None,
        is_reversed: bool = False
    ) -> DownstreamStatus:
        second_role: RoleORM = (await self.get_with_options(
            second_id, 
            (joinedload(self.model.chief))
        ))
        if first_call:
            first_role: RoleORM = self.get(first_id)
            first_level = first_role.level
            if first_id is None or second_id is None:
                if first_id is not None:
                    return DownstreamStatus.seconds_invalid
                elif second_id is not None:
                    return DownstreamStatus.first_invalid
                else:
                    return DownstreamStatus.both_invalid
        if first_level == second_role.level:
            return DownstreamStatus.false
        elif first_level < second_role.level:
            if reverse_possible:
                return await self.is_on_downstream(second_id, first_id, is_reversed=True)
            else:
                return DownstreamStatus.false
        if second_role.chief_id == first_id:
            return DownstreamStatus.upstream if is_reversed else DownstreamStatus.true
        return await self.is_on_downstream(
            first_id, 
            second_role.chief_id, 
            reverse_possible,
            first_call=False,
            first_level=first_level,
            is_reversed=is_reversed
        )
        