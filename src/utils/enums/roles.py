
from utils.enums.abstract import AEnum


class CheckRoleStatus(AEnum):
    unexist = "unexists"
    unbelonged = "unbelongs"
    belong = "belongs"
    error = "err"

    __default__ = unexist


class ViewMode(AEnum):
    info = "info"
    owner = "owner_info"
    owner_patcher = "owner_patch"
    colleague = "org_info"
    rights_patcher = "org_patch"

    __default__ = info
