from utils.enums.abstract import AEnum


class CheckProjectStatus(AEnum):
    unexist = "unexists"
    unbelonged = "unbelongs"
    belong = "belongs"
    error = "err"

    __default__ = unexist
