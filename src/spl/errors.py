from enum import Enum


class NonSingletonResultException(Exception):
    pass


class CannotGetStateLockException(Exception):
    pass


class ExitCode(Enum):
    OK = 0
    UNKNOWN_COMMAND = 1
    CANNOT_GET_STATE_LOCK = 2
