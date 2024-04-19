
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


class SendTaskVector(AEnum):
    everyone = "everyone"
    organization = "org"
    structure = "struct"
    downstream = "downstream"
    direct_down = "direct"
    nobody = False

    __default__ = direct_down


class SendPetitionVector(AEnum):
    everyone = "everyone"
    organization = "org"
    upstream = "upstream"
    structure = "struct"
    direct_up = "direct"
    nobody = False

    __default__ = upstream


class RejectTaskRight(AEnum):
    everyone = "everyone"
    structure = "struct"
    undirect = "undirect"
    same_level = "level"
    nobody = False

    __default__ = same_level


class RightsTemplateName(AEnum):
    ordinary = "ordinary"
    head = "head"
    gendir = "gendir"
    hr = "hr"
    null = None

    __default__ = ordinary


class EditOtherRight(AEnum):
    organization = "org"
    structure = "struct"
    direct = "direct"
    nobody = False

    __default__ = nobody
