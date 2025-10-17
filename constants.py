from dataclasses import dataclass

class Singleton:
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

    def __repr__(self):
        return "I am a Singleton. This is a method that supresses too few public methods linter error."


@dataclass
class Constants(Singleton):
    db_name = "database.db"
    mass_test_db_name = "mass_test.db"
    page_size = 10
    coursename_minlength = 2
    coursename_maxlength = 30
    username_minlength = 3
    username_maxlength = 30
    password_minlength = 3
    password_maxlength = 30
    course_holes_min = 1
    course_holes_default = 18
    course_holes_max = 48
    hole_par_min = 1
    hole_par_default = 3
    hole_par_max = 15
    hole_length_min = 1
    hole_length_default = 70
    hole_length_max = 500
    round_min_players = 1
    round_max_players = 10
    name_allowed_special_characters = " -=+'_()"


constants = Constants()
