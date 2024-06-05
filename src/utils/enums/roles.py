
from utils.enums.abstract import AEnum


class CheckRoleStatus(AEnum):
    unexist = "unexists"
    unbelonged = "unbelongs"
    belong = "belongs"
    forbidden = "forbidden"
    error = "err"

    __default__ = unexist


class ViewMode(AEnum):
    info = "info"
    owner = "owner_info"
    owner_patcher = "owner_patch"
    colleague = "org_info"
    rights_patcher = "org_patch"

    __default__ = info


class DownstreamStatus(AEnum):
    true = True
    upstream = "upstream"
    first_invalid = "invalid1"
    seconds_invalid = "invalid2"
    both_invalid = "invalidA"
    false = False

    __default__ = false
