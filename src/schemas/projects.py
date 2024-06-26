from datetime import datetime
import json
from typing import Annotated, ClassVar, List, Optional, Union
from uuid import UUID
from fastapi import Body, Cookie, Depends, File, Form, Query, UploadFile
from pydantic import BaseModel, Field, field_validator, model_validator

from api.dependencies import ProjectUUID
from schemas.pagination import SPaginationResponse
from schemas.rights import SHeadRights, SRoleRights
from schemas.roles import SRolePreview
from utils.enums.projects import CheckProjectStatus
from utils.enums.task import TaskStatus, TaskViewMode

COMMENT_EMPTY = "you can leave it empty"
MAX_NAME_LEN = 128  


class SAddCheckList(BaseModel):
    name: Annotated[str, Form(max_length=64)]
    checkpoints: list[str] = [] 

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        else:
            return value
    
    class Config:
        from_atributes = True


class SAddCheckListMixin(BaseModel):
    checklists: list[SAddCheckList] = Body(description=COMMENT_EMPTY, min_items=0)

    class Config:
        from_atributes = True


class SViewCheckpoints(BaseModel):
    id: UUID = None
    name: Annotated[str, Field(max_length=MAX_NAME_LEN)]
    done: bool = False

    class Config:
        from_atributes = True


class SViewChecklist(BaseModel):
    id: UUID = None
    name: Annotated[str, Field(max_length=MAX_NAME_LEN)]
    points: list[SViewCheckpoints]

    class Config:
        from_atributes = True
        

class SCreateProjectRequest(BaseModel):
    name: Annotated[str, Form(max_length=MAX_NAME_LEN)]
    desctription: Annotated[str|None, Form(max_leng=2048, default="")] = None
    deadline: datetime|None = None

    class Config:
        from_atributes = True


class SCreateTaskRequest(SCreateProjectRequest, SAddCheckListMixin):
    # files: list[UploadFile] = File(description=COMMENT_EMPTY, min_items=0)
    responsobilities: list[UUID] = Form(..., min_items=1)
    # responsobility: UUID


class SCreateTaskResponse(SCreateProjectRequest):
    id: UUID
    responsobilities: list[SRolePreview]
    creator_id: UUID
    status: Annotated[TaskStatus, Field()]
    level: int

    class Confing:
        from_atributes = True


class SCreateProjectResponse(SCreateProjectRequest):
    id: UUID
    organization_id: UUID
    creator_id: UUID
    status: str
    # status: Annotated[CheckProjectStatus, Field()]
    
    class Config:
        from_atributes = True


class SProjectPreview(BaseModel):
    _description_limit: ClassVar[int] = 50

    id: UUID
    name: str
    organization_id: UUID
    description: Annotated[str, Field(max_length=_description_limit)]
    created_at: datetime
    edited_at: datetime|None = None


class STaskPreview(SProjectPreview):
    _description_limit: ClassVar[int] = 50
    organization_id: ClassVar[None]

    id: UUID
    name: str
    description: Annotated[str, Field(max_length=_description_limit)]
    creator_name: str = None
    deadline: datetime|None = None
    created_at: datetime
    edited_at: datetime | None = None


class SMyTasksResponse(BaseModel):
    result: list[STaskPreview]
    pagination: SPaginationResponse


class SMyProjectsResponse(BaseModel):
    result: list[SProjectPreview]
    pagination: SPaginationResponse


class SProjectCheckResponce(BaseModel):
    request_key: str = None
    role_id: UUID = None
    status: Annotated[CheckProjectStatus, Field(default=CheckProjectStatus.__default__)]
    comment: str = None

    class Config:
        from_atributes = True


class SCreateSubTaskRequest(BaseModel):
    fromtask_id: Annotated[UUID, Query()]
    name: Annotated[str, Query(max_length=MAX_NAME_LEN)]
    description: Annotated[str, Query(max_length=500)]


class SCreateSubTaskResponse(BaseModel):
    task_id: Annotated[UUID, Field()]
    fromtask_id: Annotated[UUID, Field()]
    name: Annotated[str, Query(max_length=MAX_NAME_LEN)]
    description: Annotated[str, Query(max_length=500)]


class STaskPage(BaseModel):
    view_mode: Annotated[TaskViewMode, Field()]
    id: Annotated[UUID, Field()]
    name: Annotated[str, Field()]
    descripition: Annotated[str, Field()]
    status: Annotated[TaskStatus, Field()]
    deadline: Annotated[datetime|None, Field()] = None
    checklists: Annotated[list[SViewChecklist], Field()]
    responsobilities: Annotated[list[SRolePreview], Field()] = []
    # TODO implement
    # project : Annotated[SProjectPreview, Field()]
    # overtask : Annotated[STaskPreview|None, Field()]
    # subtasks : Annotated[list[STaskPreview], Field()] = []
    created_at : Annotated[datetime, Field()]
    edited_at : datetime|None = None

    class Config:
        from_atributes = True

class SPutTaskRequest(STaskPage):
    responsobilities: Annotated[list[UUID], Field()] = []
    # TODO implement
    # subtasks : Annotated[list[STaskPreview], Field()] = []