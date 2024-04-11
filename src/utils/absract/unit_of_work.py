from abc import ABC, abstractmethod
from typing import Type

from repositories.camerus import CamerusRepo
from repositories.cameras import CameraRepo
from repositories.carowners import CarOwnerRepo
from repositories.cases import CaseRepo
from repositories.export import ExportRepo
from repositories.files import FileRepo
from repositories.users import UserRepo
from repositories.violations import ViolationRepo
from repositories.votes import VoteRepo


class ABCUnitOfWork(ABC):
    cameras: Type[CameraRepo]
    camerus: Type[CamerusRepo]
    cases: Type[CaseRepo]
    car_owners: Type[CarOwnerRepo]
    export: Type[ExportRepo]
    files: Type[FileRepo]
    users: Type[UserRepo]
    violations: Type[ViolationRepo]
    votes: Type[VoteRepo]

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
