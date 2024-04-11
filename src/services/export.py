from fastapi import UploadFile
from repositories.export import ExportRepo
from utils.absract.service import BaseService
from utils.absract.unit_of_work import ABCUnitOfWork
from utils.importer import import_excel


class ExportService(BaseService):
    export_repo_dep = {repo.model.__tablename__: repo for repo in ExportRepo.__subclasses__()}
    export_tables_pattern = '|'.join(export_repo_dep.keys())

    def __init__(self, uow: ABCUnitOfWork) -> None:
        super().__init__(uow)

    async def export(self, table, file: UploadFile):
        async with self.uow:
            repository = getattr(self.uow, table, self.uow.export)
            data = import_excel(await file.read())
            result = await repository.export(data)
            await self.uow.commit()
        return result