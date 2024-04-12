from repositories.structures import StructureORM
from units_of_work._unit_of_work import UnitOfWork

class StructureUOW(UnitOfWork):
    async def __aenter__(self):
        rtrn = await super().__aenter__()
        self.structs = StructureORM(self.session)
        return rtrn

