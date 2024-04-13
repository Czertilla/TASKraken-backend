from typing import Annotated

from fastapi import Depends
from units_of_work.structure import StructureUOW
from units_of_work.user import UserUOW
from utils.absract.unit_of_work import ABCUnitOfWork

StructUOWDep = Annotated[ABCUnitOfWork, Depends(StructureUOW)]
UsersUOWDep = Annotated[ABCUnitOfWork, Depends(UserUOW)]