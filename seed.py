import datetime
import json
import random
import sqlite3
from constants import constants

db = sqlite3.connect(constants.mass_test_db_name)

db.execute("DELETE FROM participations")
db.execute("DELETE FROM course_selections")
db.execute("DELETE FROM results")
db.execute("DELETE FROM rounds")
db.execute("DELETE FROM users")
db.execute("DELETE FROM courses")

user_count = 1000
course_count = 10**5  # To put in scale Finland has somewhat over 1000 disc golf courses
rounds_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)", ["user" + str(i)])

for i in range(1, course_count + 1):
    num_holes = random.randint(constants.course_holes_min, constants.course_holes_max)

    holes_dict = {}
    for j in range(1, num_holes + 1):
        parkey = f"par_{j}"
        lengthkey = f"length_{j}"

        par = random.randint(constants.hole_par_min, constants.hole_par_max)
        length = random.randint(constants.hole_length_min, constants.hole_length_max)

        holes_dict[str(j)] = {"par": par, "length": length}

    result = db.execute(
        "INSERT INTO courses (coursename, num_holes, hole_data) VALUES (?, ?, ?)",
        ["course" + str(i), num_holes, json.dumps(holes_dict)],
    )

    course_id = result.lastrowid

    # Add selections for courses
    difficulty_select = random.randint(1, 3)
    db.execute("INSERT INTO course_selections (item_id, course_id) VALUES (?, ?)", [difficulty_select, course_id])
    type_select = random.randint(4, 6)
    db.execute("INSERT INTO course_selections (item_id, course_id) VALUES (?, ?)", [type_select, course_id])


for _ in range(1, rounds_count + 1):
    creator_id = random.randint(1, user_count)
    start_time = datetime.datetime.now().isoformat(timespec="minutes")
    num_players = random.randint(constants.round_min_players, constants.round_max_players)
    coursename = "course" + str(random.randint(1, course_count))
    num_holes = random.randint(constants.course_holes_min, constants.course_holes_max)

    holes_dict = {}
    for i in range(1, num_holes + 1):
        parkey = f"par_{i}"
        lengthkey = f"length_{i}"

        par = random.randint(constants.hole_par_min, constants.hole_par_max)
        length = random.randint(constants.hole_length_min, constants.hole_length_max)

        holes_dict[str(i)] = {"par": par, "length": length}

    result = db.execute(
        """INSERT INTO rounds (creator_id, start_time, num_players, coursename, num_holes, hole_data)
                  VALUES (?, ?, ?, ?, ?, ?)""",
        [creator_id, start_time, num_players, coursename, num_holes, json.dumps(holes_dict)],
    )

    round_participations = random.randint(0, num_players - constants.round_min_players)
    round_id = result.lastrowid

    # Add result for round creator
    for i in range(1, num_holes + 1):
        hole_result = random.randint(constants.hole_par_min, constants.hole_par_max)

        db.execute(
            """INSERT INTO results (round_id, player_id, hole, result)
                    VALUES (?, ?, ?, ?)""",
            [round_id, creator_id, i, hole_result],
        )

    # Add round participations
    for _ in range(0, round_participations):
        participator_id = random.randint(1, user_count)

        while participator_id == creator_id:
            participator_id = random.randint(1, user_count)

        db.execute(
            """INSERT INTO participations (round_id, participator_id)
                    VALUES (?, ?)""",
            [round_id, participator_id],
        )

        # Add result for participator
        for i in range(1, num_holes + 1):
            hole_result = random.randint(constants.hole_par_min, constants.hole_par_max)

            db.execute(
                """INSERT INTO results (round_id, player_id, hole, result)
                        VALUES (?, ?, ?, ?)""",
                [round_id, participator_id, i, hole_result],
            )

db.commit()
db.close()
