
from utils.enums.abstract import AEnum


class CreateStructRight(AEnum):
    in_organization = "org"
    in_overstruct = "overstruct"
    in_struct = "struct"
    nowhere = False

    __default__ = nowhere


class CreateVacancyRigth(AEnum):
    organization = "org"
    in_overstructure = "ovestruct"
    lower_level = "level"
    in_structure = "struct"
    downstream = "downstream"
    subordinates = "subord"
    nobody = False

    __default__ = nobody


class TaskSendVector(AEnum):
    everyone = "everyone"
    direct = "direct"
    structure = "struct"
    organization = "org"
    nobody = False

    ALL = "ALL"

    __default__ = direct


class PetitionSendVector(AEnum):    
    everyone = "everyone"
    organization = "org"
    upstream = "upstream"
    structure = "struct"
    direct = "direct"
    nobody = False

    __default__ = upstream


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