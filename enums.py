from enum import Enum, StrEnum, auto


class SelectionItemClass(StrEnum):
    COURSE_DIFFICULTY = auto()
    COURSE_TYPE = auto()


class FlashCategory(StrEnum):
    MESSAGE = auto()
    ERROR = auto()
    INFO = auto()
    WARNING = auto()


class FindRoundParam(Enum):
    DATE = 1
    COURSENAME = 2
    CREATORID = 3
    ROUNDID = 4
    PARTICIPATORID = 5


class RespType(Enum):
    DEFAULT = 1
    DICT = 2

class QueryType(Enum):
    ONE = 1
    ALL = 2
