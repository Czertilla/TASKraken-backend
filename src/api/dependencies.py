from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Depends
from units_of_work.projects import ProjectUOW
from units_of_work.roles import RoleUOW
from units_of_work.structure import StructureUOW
from units_of_work.tasks import TaskUOW
from units_of_work.user import UserUOW
from utils.absract.unit_of_work import ABCUnitOfWork


RoleUUID = Annotated[UUID, Cookie()]
ProjectUUID = Annotated[UUID, Cookie()]
TaskUUID = Annotated[UUID, Cookie()]

StructUOWDep = Annotated[ABCUnitOfWork, Depends(StructureUOW)]
UsersUOWDep = Annotated[ABCUnitOfWork, Depends(UserUOW)]
RoleUOWDep = Annotated[ABCUnitOfWork, Depends(RoleUOW)]
ProjectUOWDep = Annotated[ABCUnitOfWork, Depends(ProjectUOW)]
TaskUOWDep = Annotated[ABCUnitOfWork, Depends(TaskUOW)]
