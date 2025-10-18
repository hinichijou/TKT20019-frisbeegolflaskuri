from enum import Enum, StrEnum, auto


class SelectionItemClass(StrEnum):
    COURSE_DIFFICULTY = auto()
    COURSE_TYPE = auto()


class FlashCategory(StrEnum):
    MESSAGE = auto()
    ERROR = auto()
    INFO = auto()
    WARNING = auto()


class NavPageCategory(StrEnum):
    DEFAULT = auto()
    INDEX = auto()
    NEW_COURSE = auto()
    SHOW_COURSES = auto()
    NEW_ROUND = auto()
    FIND_ROUND = auto()
    REGISTER = auto()
    LOGIN = auto()
    FIND_COURSE = auto()


class FindRoundParam(Enum):
    DATE_LIKE = 1
    COURSENAME = 2
    CREATORID = 3
    ROUNDID = 4
    CREATORNAME = 5
    DATE_NOW_OR_AFTER = 6
    DATE_BEFORE = 7


class FindCourseParam(Enum):
    COURSENAME = 1
    NUM_HOLES = 2
    DIFFICULTY = 3
    TYPE = 4


class RespType(Enum):
    DEFAULT = 1
    DICT = 2


class QueryType(Enum):
    ONE = 1
    ALL = 2


class ResultCategory(StrEnum):
    DEFAULT = auto()
    EAGLE = auto()
    BIRDIE = auto()
    PAR = auto()
    BOGEY = auto()
    DOUBLEBOGEY = auto()


class InputCategory(Enum):
    USERNAME = 1
    COURSENAME = 2
