from enum import Enum


class AEnum(Enum):
    def _missing_(cls, value):
        return cls.default
