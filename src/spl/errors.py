from enum import Enum


class ExitCode(Enum):
    OK = 0
    UNKNOWN_COMMAND = 1
    CANNOT_GET_STATE_LOCK = 2
    NON_SINGLETON_RESULT = 3
    UNINSTALLABLE = 4


class NonSingletonResultException(Exception):
    exit_code = ExitCode.NON_SINGLETON_RESULT


class CannotGetStateLockException(Exception):
    exit_code = ExitCode.CANNOT_GET_STATE_LOCK


class NotDownloadableException(Exception):
    exit_code = ExitCode.UNINSTALLABLE
