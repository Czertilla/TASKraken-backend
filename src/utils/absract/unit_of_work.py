from abc import ABC, abstractmethod
from typing import Type

from repositories.files import FileRepo
from repositories.roles import RoleRepo
from repositories.structures import StructureRepo
from repositories.users import UserRepo


class ABCUnitOfWork(ABC):
    files: Type[FileRepo]
    users: Type[UserRepo]
    roles: Type[RoleRepo]
    structs: Type[StructureRepo]

    @abstractmethod
    def __init__(self):
        raise NotImplementedError


    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError
    

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError


    @abstractmethod
    async def commit(self):
        raise NotImplementedError
    

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
