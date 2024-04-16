
from utils.enums.abstract import AEnum


class TaskStatus(AEnum):
    created = "created"
    frozen = "frozen"
    resumed = "resumed"
    closed = "closed"
    completed = "completed"

    default = created