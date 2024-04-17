
from utils.enums.abstract import AEnum


class TaskSendVector(AEnum):
    everyone = "everyone"
    direct = "direct"
    structure = "struct"
    organization = "org"
    nobody = False

    ALL = "ALL"

    __default__ = direct

class RejectRight(AEnum):
    same_level = "level"
    undirect = "undirect"
    structure = "struct"
    everyone = "everyone"
    nobody = False

    __default__ = same_level


class RightsTemplateName(AEnum):
    ordinary = "ordinary"
    head = "head"
    gendir = "gendir"
    hr = "hr"
    null = None

    __default__ = ordinary