from typing import Annotated
from fastapi import Query
from pydantic import BaseModel
from utils.enums.abstract import AEnum
from utils.enums.rights import CreateStructRight, CreateVacancyRigth, EditOtherRight, RejectTaskRight, RightsTemplateName, SendPetitionVector, SendTaskVector


class SRoleRights(BaseModel):
    template: Annotated[RightsTemplateName, Query(default=RightsTemplateName.__default__)]
    can_create_substructures: Annotated[CreateStructRight, Query(default=CreateStructRight.__default__)]
    can_create_subordinates: Annotated[CreateVacancyRigth, Query(default=CreateVacancyRigth.__default__)]
    can_send_task: Annotated[SendTaskVector, Query(default=SendTaskVector.__default__)]
    can_send_report: Annotated[bool, Query(default=True)]
    can_send_petition: Annotated[SendPetitionVector, Query(default=SendPetitionVector.__default__)]
    can_reject_task: Annotated[RejectTaskRight, Query(default=RejectTaskRight.__default__)]
    can_create_project: Annotated[bool, Query(default=False)]
    can_edit_other_rights: Annotated[EditOtherRight, Query(default=EditOtherRight.__default__)]
    can_edit_oneself_rights: Annotated[bool, Query(default=False)]


    class Config:
        from_attributes = True


class SGenDirRights(SRoleRights):
    template: Annotated[RightsTemplateName, Query(default=RightsTemplateName.gendir)]
    can_create_substructures: Annotated[CreateStructRight, Query(default=CreateStructRight.in_organization)]
    can_create_subordinates: Annotated[CreateVacancyRigth, Query(default=CreateVacancyRigth.organization)]
    can_send_task: Annotated[SendTaskVector, Query(default=SendTaskVector.everyone)]
    can_send_report: Annotated[bool, Query(default=True)]
    can_send_petition: Annotated[SendPetitionVector, Query(default=SendPetitionVector.everyone)]
    can_reject_task: Annotated[RejectTaskRight, Query(default=RejectTaskRight.everyone)]
    can_create_project: Annotated[bool, Query(default=True)]
    can_edit_other_rights: Annotated[EditOtherRight, Query(default=EditOtherRight.organization)]
    can_edit_oneself_rights: Annotated[bool, Query(default=True)]


class SHeadRights(SRoleRights):
    template: Annotated[RightsTemplateName, Query(default=RightsTemplateName.head)]
    can_create_subordinates: Annotated[CreateVacancyRigth, Query(default=CreateVacancyRigth.organization)]
    can_edit_other_rights: Annotated[EditOtherRight, Query(default=EditOtherRight.organization)]
    can_edit_oneself_rights: Annotated[bool, Query(default=True)]
