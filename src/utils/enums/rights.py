
from utils.enums.abstract import AEnum


class TaskSendVector(AEnum):
    everyone = "everyone"
    direct = "direct"
    structure = "struct"
    organization = "org"

    ALL = "ALL"
    nobody = False

    default = direct

class RejectRight(AEnum):
    same_level = "level"
    undirect = "undirect"
    structure = "struct"
    everyone = "everyone"
    nobody = False

    default = same_level
