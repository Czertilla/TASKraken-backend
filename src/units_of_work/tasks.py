from repositories.checklists import CheckListRepo
from repositories.files import FileRepo, FolderRepo
from repositories.rights import RightRepo
from repositories.roles import RoleRepo
from repositories.tasks import TaskRepo
from repositories.users import UserRepo
from units_of_work._unit_of_work import UnitOfWork

class TaskUOW(UnitOfWork):
    async def __aenter__(self):
        rtrn = await super().__aenter__()
        self.files = FileRepo(self.session)
        self.folders = FolderRepo(self.session)
        self.roles = RoleRepo(self.session)
        self.checklists = CheckListRepo(self.session)
        self.tasks = TaskRepo(self.session)
        return rtrn
