import datetime
import json
import random
import sqlite3
from constants import constants

db = sqlite3.connect(constants.mass_test_db_name)

db.execute("DELETE FROM users")
db.execute("DELETE FROM courses")
db.execute("DELETE FROM rounds")

user_count = 1000
course_count = 10**5 # To put in scale Finland has somewhat over 1000 disc golf courses
rounds_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, course_count + 1):
    num_holes = random.randint(constants.course_holes_min, constants.course_holes_max)

    holes_dict = {}
    for j in range(1, num_holes):
        parkey = f"par_{j}"
        lengthkey = f"length_{j}"

        par = random.randint(constants.hole_par_min, constants.hole_par_max)
        length = random.randint(constants.hole_length_min, constants.hole_length_max)

        holes_dict[str(j)] = {"par": par, "length": length}

    db.execute("INSERT INTO courses (coursename, num_holes, hole_data) VALUES (?, ?, ?)",
               ["course" + str(i), num_holes, json.dumps(holes_dict)])

for i in range(1, rounds_count + 1):
    creator_id = random.randint(1, user_count)
    start_time = datetime.datetime.now().isoformat(timespec="minutes")
    num_players = random.randint(constants.round_min_players, constants.round_max_players)
    coursename = "course" + str(random.randint(1, course_count))
    num_holes = random.randint(constants.course_holes_min, constants.course_holes_max)

    holes_dict = {}
    for j in range(1, num_holes):
        parkey = f"par_{j}"
        lengthkey = f"length_{j}"

        par = random.randint(constants.hole_par_min, constants.hole_par_max)
        length = random.randint(constants.hole_length_min, constants.hole_length_max)

        holes_dict[str(j)] = {"par": par, "length": length}

    db.execute("""INSERT INTO rounds (creator_id, start_time, num_players, coursename, num_holes, hole_data)
                  VALUES (?, ?, ?, ?, ?, ?)""",
               [creator_id, start_time, num_players, coursename, num_holes, json.dumps(holes_dict) ])

db.commit()
db.close()
