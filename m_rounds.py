import json
import db
import m_courses
from enums import FindRoundParam
from utilities import format_date_from_iso

default_format_options = {"start_time": True, "hole_data": True}

def add_round(course_id, creator, start_time, num_players):
    course_data = m_courses.get_course_data(course_id, format_options={"hole_data": False})

    if course_data:
        sql = "INSERT INTO rounds (coursename, num_holes, hole_data, creator_id, start_time, num_players) VALUES (?, ?, ?, ?, ?, ?)"
        db.execute(sql, [course_data["coursename"], course_data["num_holes"], course_data["hole_data"], creator, start_time, num_players])
        return db.last_insert_id()
    else:
        #TODO: Virheilmoitus
        print(f"VIRHE: Rataa id:llä {course_id} ei löytynyt tietokannasta. Uutta kierrosta ei luotu")
        return None

def delete_round(round_id):
    delete_participation(round_id)

    sql = "DELETE FROM rounds WHERE id = ?"
    db.execute(sql, [round_id])

def update_round(data):
    sql = "UPDATE rounds SET coursename = ?, num_holes = ?, hole_data = ?, creator_id = ?, start_time = ?, num_players = ? WHERE id = ?"
    db.execute(sql, [data["coursename"], data["num_holes"], json.dumps(data["hole_data"]), data["user_id"], data["start_time"], data["num_players"], data["id"]])


def get_all_rounds(format_options = default_format_options):
    sql = "SELECT rounds.id, coursename, username, start_time, num_players, " \
            "IFNULL(COUNT(participations.participator_id) + 1, 1) AS num_participating " \
            "FROM rounds " \
            "JOIN users ON users.id=rounds.creator_id " \
            "LEFT JOIN participations ON participations.round_id=rounds.id " \
            "GROUP BY rounds.id"

    rounds = db.query_db(sql, resp_type = db.RespType.DICT)

    if not rounds:
        rounds = []
    else:
        format_rounds(rounds, format_options)

    return rounds

def get_round(id, format_options = default_format_options):
    sql = "SELECT rounds.id as round_id, creator_id, coursename, num_holes, hole_data, start_time, num_players, " \
            "GROUP_CONCAT(users.id) AS user_ids, " \
            "GROUP_CONCAT(users.username) AS usernames " \
            "FROM rounds " \
            "LEFT JOIN participations ON participations.round_id=rounds.id " \
            "JOIN users ON users.id IN (rounds.creator_id, participations.participator_id) " \
            "WHERE rounds.id = ? " \
            "GROUP BY rounds.id"
    result = db.query_db(sql, [id], db.RespType.DICT)
    return format_rounds(result, format_options)[0] if result else result

def get_sql_for_param(param):
    match(param):
        case FindRoundParam.DATE:
            return "start_time LIKE ?"
        case FindRoundParam.COURSENAME:
            return "coursename = ?"
        case FindRoundParam.CREATORID:
            return "creator_id = ?"
        case FindRoundParam.ROUNDID:
            return "rounds.id = ?"
        case FindRoundParam.PARTICIPATORID:
            return "participations.participator_id = ?"
        case _:
            return ""

def create_where_condition(params):
    where = ""

    for i in range(len(params)):
        if i == 0:
            where += "WHERE " + get_sql_for_param(params[i]) + " "
        else:
            where += "AND " + get_sql_for_param(params[i]) + " "

    return where

def find_rounds(searchparams, format_options = default_format_options):
    types, params = zip(*searchparams)
    where = create_where_condition(types)
    sql = "SELECT rounds.id, coursename, username, start_time, num_players, " \
            "IFNULL(COUNT(participations.participator_id) + 1, 1) AS num_participating " \
            "FROM rounds " \
            "JOIN users ON users.id=rounds.creator_id " \
            "LEFT JOIN participations ON participations.round_id=rounds.id " \
            + where + \
            "GROUP BY rounds.id " \
            "ORDER BY start_time DESC"
    result = db.query_db(sql, params, resp_type = db.RespType.DICT)
    return format_rounds(result, format_options) if result else result

def get_user_id_for_round(round_id):
    sql = "SELECT rounds.id, users.id AS user_id FROM rounds JOIN users ON users.id=rounds.creator_id WHERE rounds.id = ?"
    result = db.query_db(sql, [round_id])
    return result[0]["user_id"] if result else result

def format_rounds(rounds, format_options):
    for row in rounds:
        if format_options["start_time"] and "start_time" in row:
            row["start_time"] = format_date_from_iso(row["start_time"])
        if format_options["hole_data"] and "hole_data" in row:
            row["hole_data"] = json.loads(row["hole_data"])
        if "user_ids" in row and "usernames" in row:
            user_ids = row["user_ids"].split(",")
            usernames = row["usernames"].split(",")
            if len(user_ids) == len(usernames):
                row["participators"] = {int(user_ids[i]): usernames[i] for i in range(len(user_ids))}

    return rounds

def add_participation(round_id, user_id):
    sql = "INSERT INTO participations (round_id, participator_id) VALUES (?, ?)"
    db.execute(sql, [round_id, user_id])

def delete_participation(round_id, user_id = ""):
    sql = "DELETE FROM participations WHERE round_id = ?"
    params = [round_id]
    if user_id:
        sql += "AND participator_id = ?"
        params.append(user_id)

    db.execute(sql, params)