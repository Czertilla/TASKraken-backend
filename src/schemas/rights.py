from typing import Annotated
from fastapi import Query
from pydantic import BaseModel
from utils.enums.abstract import AEnum
from utils.enums.rights import RejectRight, TaskSendVector


class RightsTemplateName(AEnum):
    ordinary = "ordinary"
    head = "head"
    gendir = "gendir"
    hr = "hr"
    null = None

    default = ordinary


class SRoleRights(BaseModel):
    template: Annotated[RightsTemplateName, Query(default=RightsTemplateName.default)]
    can_create_substructures: Annotated[bool, Query(default=False)]
    can_create_subordinates: Annotated[bool, Query(default=False)]
    can_send_task: Annotated[TaskSendVector, Query(default=TaskSendVector.default)]
    can_send_report: Annotated[bool, Query(default=True)]
    can_reject_task: Annotated[RejectRight, Query(default=RejectRight.default)]

    class Config:
        from_attributes = True


class SGenDirRights(SRoleRights):
    template: Annotated[RightsTemplateName, Query(default=RightsTemplateName.gendir)]
    can_create_substructures: Annotated[bool, Query(default=True)]
    can_create_subordinates: Annotated[bool, Query(default=True)]
    can_send_task: Annotated[TaskSendVector, Query(default=TaskSendVector.organization)]
    can_reject_task: Annotated[RejectRight, Query(default=RejectRight.everyone)]


class SHeadRights(SRoleRights):
    template: Annotated[RightsTemplateName, Query(default=RightsTemplateName.head)]
    can_create_substructures: Annotated[bool, Query(default=True)]
    can_create_subordinates: Annotated[bool, Query(default=True)]
    can_send_task: Annotated[TaskSendVector, Query(default=TaskSendVector.structure)]
    can_reject_task: Annotated[RejectRight, Query(default=RejectRight.same_level)]

