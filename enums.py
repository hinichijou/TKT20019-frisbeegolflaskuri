from enum import Enum, StrEnum, auto

class SelectionItemClass(StrEnum):
    COURSE_DIFFICULTY = auto(),
    COURSE_TYPE = auto()

class FindRoundParam(Enum):
    DATE = 1,
    COURSENAME = 2,
    CREATORID = 3,
    ROUNDID = 4,
    PARTICIPATORID = 5