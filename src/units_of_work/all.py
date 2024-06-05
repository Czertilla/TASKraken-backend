from repositories.files import FileRepo, FolderRepo
from repositories.projects import ProjectRepo
from repositories.rights import RightRepo
from repositories.roles import RoleRepo
from repositories.structures import StructureRepo
from repositories.tasks import TaskRepo
from repositories.users import UserRepo
from units_of_work._unit_of_work import UnitOfWork

class AllUOW(UnitOfWork):
    async def __aenter__(self):
        rtrn = await super().__aenter__()
        
        self.files = FileRepo(self.session)
        self.folders = FolderRepo(self.session)
        self.users = UserRepo(self.session)
        self.roles = RoleRepo(self.session)
        self.rights = RightRepo(self.session)
        self.structs = StructureRepo(self.session)
        self.projects = ProjectRepo(self.session)
        self.tasks = TaskRepo(self.session)
        
        return rtrn
