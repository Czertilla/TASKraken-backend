from repositories.files import FileRepo
from repositories.rights import RightRepo
from repositories.roles import RoleRepo
from repositories.users import UserRepo
from units_of_work._unit_of_work import UnitOfWork

class RoleUOW(UnitOfWork):
    async def __aenter__(self):
        rtrn = await super().__aenter__()
        self.files = FileRepo(self.session)
        self.roles = RoleRepo(self.session)
        self.users = UserRepo(self.session)
        self.rights = RightRepo(self.session)
        return rtrn