import json
import datetime
import db
import m_courses

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
            "LEFT JOIN participations ON participations.round_id=rounds.id AND rounds.id IS NOT NULL " \
            "GROUP BY rounds.id"
    return db.query_dict(sql)

def get_all_rounds():
    rounds = get_rounds_dict()
    if not rounds:
        rounds = []
    else:
        for row in rounds:
            row["start_time"] = datetime.datetime.fromisoformat(row["start_time"]).strftime("%d/%m/%Y %H:%M")

    return rounds