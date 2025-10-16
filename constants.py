from dataclasses import dataclass
from utilities import Singleton


@dataclass
class Constants(Singleton):
    db_name = "database.db"
    mass_test_db_name = "mass_test_one_by_one_indices.db"
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


constants = Constants()
