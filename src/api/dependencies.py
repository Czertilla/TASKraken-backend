from typing import Annotated

from fastapi import Depends
from units_of_work.user import UserUOW
from utils.absract.unit_of_work import ABCUnitOfWork


UsersUOWDep = Annotated[ABCUnitOfWork, Depends(UserUOW)]