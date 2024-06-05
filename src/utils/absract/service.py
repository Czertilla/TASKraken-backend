from math import ceil
from schemas.pagination import SPaginationRequest
from utils.absract.unit_of_work import ABCUnitOfWork


class BaseService:
    def __init__(self, uow: ABCUnitOfWork) -> None:
        self.uow = uow

    def get_total_pagination(self, length: int, size: int)-> int:
        return ceil(length / size) - 1


    def get_offset(self, pagination: SPaginationRequest)->tuple[int]:
        return (
            pagination.page * pagination.size,
            (pagination.page + 1) * pagination.size
        )
