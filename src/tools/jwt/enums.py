from enum import Enum


class TokenPurpose(str, Enum):
    access = "access"
    refresh = "refresh"
