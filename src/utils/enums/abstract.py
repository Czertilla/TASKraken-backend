from enum import Enum


class AEnum(Enum):
    __default__ = None

    def _missing_(cls, value):
        return cls.__default__
