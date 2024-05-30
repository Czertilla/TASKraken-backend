
from utils.enums.abstract import AEnum


class TaskStatus(AEnum):
    created = "created"
    frozen = "frozen"
    resumed = "resumed"
    closed = "closed"
    completed = "completed"

    __default__ = created


class TaskViewMode(AEnum):
    responsible = "responsible"
    creator = "creator"
    rejected = "rejected"
    error = "error"

    __default__ = rejected
