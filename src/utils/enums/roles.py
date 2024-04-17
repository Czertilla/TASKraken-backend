
from utils.enums.abstract import AEnum


class CheckRoleStatus(AEnum):
    unexist = "unexists"
    unbelonged ="unbelongs"
    belong = "belongs"

    __default__ = unexist


class ViewMode(AEnum):
    info = "info"
    owner = "owner"
    chief = "chief"
    patch = "patch"

    __default__ = info
