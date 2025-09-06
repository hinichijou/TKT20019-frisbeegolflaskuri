import json
import db
import m_courses
from utilities import format_date_from_iso

def add_round(course_id, creator, start_time, num_players):
    course_data = m_courses.get_course_data_dict(course_id)

    if course_data:
        sql = "INSERT INTO rounds (coursename, num_holes, hole_data, creator_id, start_time, num_players) VALUES (?, ?, ?, ?, ?, ?)"
        db.execute(sql, [course_data["coursename"], course_data["num_holes"], course_data["holes"], creator, start_time, num_players])
    else:
        #TODO: Virheilmoitus
        print(f"VIRHE: Rataa id:llä {course_id} ei löytynyt tietokannasta. Uutta kierrosta ei luotu")

def get_rounds_dict():
    sql = "SELECT rounds.id, coursename, username, start_time, num_players, IFNULL(SUM(participations.participator_id) + 1, 1) AS num_participating FROM rounds " \
            "JOIN users ON users.id=rounds.creator_id " \
            "LEFT JOIN participations ON participations.round_id=rounds.id " \
            "GROUP BY rounds.id"
    return db.query_dict(sql)

def get_all_rounds():
    rounds = get_rounds_dict()

    if not rounds:
        rounds = []
    else:
        format_rounds(rounds)

    return rounds

def get_round(id):
    sql = "SELECT coursename, num_holes, hole_data, username, start_time, num_players, IFNULL(SUM(participations.participator_id) + 1, 1) AS num_participating FROM rounds " \
            "JOIN users ON users.id IN (rounds.creator_id, participations.participator_id) " \
            "LEFT JOIN participations ON participations.round_id=rounds.id " \
            "WHERE rounds.id = ?"
    result = db.query_dict(sql, [id])
    return format_rounds(result)[0] if result else result

def format_rounds(rounds):
    for row in rounds:
        if "start_time" in row:
            row["start_time"] = format_date_from_iso(row["start_time"])
        if "hole_data" in row:
            row["hole_data"] = json.loads(row["hole_data"])

    return rounds