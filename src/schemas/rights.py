from typing import Annotated
from fastapi import Query
from pydantic import BaseModel
from utils.enums.abstract import AEnum
from utils.enums.rights import RejectTaskRight, RightsTemplateName, SendTaskVector


class SRoleRights(BaseModel):
    template: Annotated[RightsTemplateName, Query(default=RightsTemplateName.__default__)]
    can_create_substructures: Annotated[bool, Query(default=False)]
    can_create_subordinates: Annotated[bool, Query(default=False)]
    can_send_task: Annotated[SendTaskVector, Query(default=SendTaskVector.__default__)]
    can_send_report: Annotated[bool, Query(default=True)]
    can_reject_task: Annotated[RejectTaskRight, Query(default=RejectTaskRight.__default__)]

    class Config:
        from_attributes = True


class SGenDirRights(SRoleRights):
    template: Annotated[RightsTemplateName, Query(default=RightsTemplateName.gendir)]
    can_create_substructures: Annotated[bool, Query(default=True)]
    can_create_subordinates: Annotated[bool, Query(default=True)]
    can_send_task: Annotated[SendTaskVector, Query(default=SendTaskVector.organization)]
    can_reject_task: Annotated[RejectTaskRight, Query(default=RejectTaskRight.everyone)]


class SHeadRights(SRoleRights):
    template: Annotated[RightsTemplateName, Query(default=RightsTemplateName.head)]
    can_create_substructures: Annotated[bool, Query(default=True)]
    can_create_subordinates: Annotated[bool, Query(default=True)]
    can_send_task: Annotated[SendTaskVector, Query(default=SendTaskVector.structure)]
    can_reject_task: Annotated[RejectTaskRight, Query(default=RejectTaskRight.same_level)]

