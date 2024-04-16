from repositories.roles import RoleRepo
from repositories.structures import StructureRepo
from units_of_work._unit_of_work import UnitOfWork

class StructureUOW(UnitOfWork):
    async def __aenter__(self):
        rtrn = await super().__aenter__()
        self.structs = StructureRepo(self.session)
        self.roles = RoleRepo(self.session)
        return rtrn

