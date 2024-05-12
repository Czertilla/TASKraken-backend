from abc import ABC, abstractmethod
from typing import Type

from repositories.files import FileRepo, FolderRepo
from repositories.projects import ProjectRepo
from repositories.rights import RightRepo
from repositories.roles import RoleRepo
from repositories.structures import StructureRepo
from repositories.tasks import TaskRepo
from repositories.users import UserRepo


class ABCUnitOfWork(ABC):
    files: Type[FileRepo]
    folders: Type[FolderRepo]
    users: Type[UserRepo]
    roles: Type[RoleRepo]
    rights: Type[RightRepo]
    structs: Type[StructureRepo]
    projects: Type[ProjectRepo]
    tasks: Type[TaskRepo]

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
