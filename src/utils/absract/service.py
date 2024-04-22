from schemas.pagination import SPaginationRequest
from utils.absract.unit_of_work import ABCUnitOfWork


class BaseService:
    def __init__(self, uow: ABCUnitOfWork) -> None:
        self.uow = uow

    def get_offset(self, pagination: SPaginationRequest)->tuple[int]:
        return (
            pagination.page * pagination.size,
            (pagination.page + 1) * pagination.size
        )
