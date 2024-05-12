from repositories.files import FileRepo, FolderRepo
from repositories.projects import ProjectRepo
from repositories.rights import RightRepo
from repositories.roles import RoleRepo
from repositories.tasks import TaskRepo
from repositories.users import UserRepo
from units_of_work._unit_of_work import UnitOfWork

class ProjectUOW(UnitOfWork):
    async def __aenter__(self):
        rtrn = await super().__aenter__()
        self.roles = RoleRepo(self.session)
        self.projects = ProjectRepo(self.session)
        self.tasks = TaskRepo(self.session)
        self.files = FileRepo(self.session)
        self.folders = FolderRepo(self.session)
        return rtrn
