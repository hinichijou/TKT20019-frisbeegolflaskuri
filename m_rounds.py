import datetime
import json
import db
import m_courses
import m_results
from enums import FindRoundParam
from utilities import use_default_if_list_none, get_page_limit_and_offset, create_where_condition

default_format_options = {"hole_data": True}


def add_round(course_id, creator, start_time, num_players):
    course_data = m_courses.get_course_data(course_id, format_options={"hole_data": False})

    if course_data:
        sql = (
            "INSERT INTO rounds (coursename, num_holes, hole_data, creator_id, start_time, num_players) "
            "VALUES (?, ?, ?, ?, ?, ?)"
        )
        db.execute(
            sql,
            [
                course_data["coursename"],
                course_data["num_holes"],
                course_data["hole_data"],
                creator,
                start_time,
                num_players,
            ],
        )
        return db.last_insert_id()
    else:
        return None


def delete_round(round_id):
    delete_participation(round_id)
    m_results.delete_results_for_round(round_id)

    sql = "DELETE FROM rounds WHERE id = ?"
    db.execute(sql, [round_id])


def update_round(data):
    sql = (
        "UPDATE rounds "
        "SET coursename = ?, num_holes = ?, hole_data = ?, creator_id = ?, start_time = ?, num_players = ? "
        "WHERE id = ?"
    )
    db.execute(
        sql,
        [
            data["coursename"],
            data["num_holes"],
            json.dumps(data["hole_data"]),
            data["user_id"],
            data["start_time"],
            data["num_players"],
            data["id"],
        ],
    )


def get_all_rounds(page, page_size, only_future_rounds=False):
    sql = (
        "SELECT rounds.id, coursename, username, start_time, num_players, "
        "IFNULL(COUNT(participations.participator_id) + 1, 1) AS num_participating "
        "FROM rounds "
        "JOIN users ON users.id=rounds.creator_id "
        "LEFT JOIN participations ON participations.round_id=rounds.id "
    )

    if only_future_rounds:
        sql = sql + "WHERE start_time >= ? "

    sql = sql + "GROUP BY rounds.id ORDER BY start_time LIMIT ? OFFSET ?"

    limit, offset = get_page_limit_and_offset(page, page_size)
    params = [limit, offset]
    if only_future_rounds:
        params.insert(0, datetime.datetime.now().isoformat(timespec="minutes"))

    rounds = db.fetch_all_from_db(sql, params, resp_type=db.RespType.DICT)

    if not rounds:
        rounds = []
    else:
        format_rounds(rounds)

    return rounds


def get_round(round_id):
    sql = (
        "SELECT rounds.id as round_id, creator_id, coursename, num_holes, hole_data, start_time, num_players, "
        "GROUP_CONCAT(users.id) AS user_ids, "
        "GROUP_CONCAT(users.username) AS usernames "
        "FROM rounds "
        "LEFT JOIN participations ON participations.round_id=rounds.id "
        "JOIN users ON users.id IN (rounds.creator_id, participations.participator_id) "
        "WHERE rounds.id = ? "
        "GROUP BY rounds.id"
    )
    result = db.fetch_all_from_db(sql, [round_id], db.RespType.DICT)
    return format_rounds(result)[0] if result else result


def get_sql_for_param(param):
    match param:
        case FindRoundParam.DATE_LIKE:
            return "start_time LIKE ?"
        case FindRoundParam.COURSENAME:
            return "coursename LIKE ?"
        case FindRoundParam.CREATORID:
            return "creator_id = ?"
        case FindRoundParam.ROUNDID:
            return "rounds.id = ?"
        case FindRoundParam.CREATORNAME:
            return "username LIKE ?"
        case FindRoundParam.DATE_NOW_OR_AFTER:
            return "start_time >= ?"
        case FindRoundParam.DATE_BEFORE:
            return "start_time < ?"
        case _:
            return ""


def find_rounds(searchparams, page, page_size):
    types, params = zip(*searchparams)
    params = params + get_page_limit_and_offset(page, page_size)
    where = create_where_condition(types, get_sql_for_param)
    sql = (
        "SELECT rounds.id, coursename, username, start_time, num_players, "
        "IFNULL(COUNT(participations.participator_id) + 1, 1) AS num_participating "
        "FROM rounds "
        "JOIN users ON users.id=rounds.creator_id "
        "LEFT JOIN participations ON participations.round_id=rounds.id " + where + "GROUP BY rounds.id "
        "ORDER BY start_time "
        "LIMIT ? OFFSET ?"
    )
    result = db.fetch_all_from_db(sql, params, resp_type=db.RespType.DICT)
    return format_rounds(result) if result else result


def get_user_id_for_round(round_id):
    sql = (
        "SELECT rounds.id, users.id AS user_id FROM rounds JOIN users ON users.id=rounds.creator_id WHERE rounds.id = ?"
    )
    result = db.fetch_all_from_db(sql, [round_id])
    return result[0]["user_id"] if result else result


# Params None returns count of all rounds
def round_count(searchparams=None):
    params = None
    sql = "SELECT COUNT(rounds.id) FROM rounds"

    if searchparams:
        types, params = zip(*searchparams)
        if FindRoundParam.CREATORNAME in types:
            sql += " JOIN users ON users.id=rounds.creator_id"
        where = create_where_condition(types, get_sql_for_param).rstrip()
        if where:
            sql += f" {where}"

    result = db.fetch_one_from_db(sql, params)
    return result[0] if result else 0


# Format options is a bad choice in retrospect, better to have the data always in consistent
# format and handle in component logic. Think about refactoring.
def format_rounds(rounds, format_options=None):
    format_options = use_default_if_list_none(format_options, default=default_format_options)

    for row in rounds:
        if format_options["hole_data"] and "hole_data" in row:
            row["hole_data"] = json.loads(row["hole_data"])
        # The join in SQL query made id to be ambiguous, but its better that id can be found
        # consistently from all round query responses. And round.id makes sense in terms of naming.
        if "round_id" in row:
            row["id"] = row["round_id"]
        if "user_ids" in row and "usernames" in row:
            user_ids = row["user_ids"].split(",")
            usernames = row["usernames"].split(",")
            if len(user_ids) == len(usernames):
                row["participators"] = {int(user_ids[i]): usernames[i] for i in range(len(user_ids))}

    return rounds


def add_participation(round_id, user_id):
    sql = "INSERT INTO participations (round_id, participator_id) VALUES (?, ?)"
    db.execute(sql, [round_id, user_id])


def delete_participation(round_id, user_id=""):
    sql = "DELETE FROM participations WHERE round_id = ?"
    params = [round_id]
    if user_id:
        sql += "AND participator_id = ?"
        params.append(user_id)

    db.execute(sql, params)


def user_participations_count(user_id, timeparam):
    sql =  (
        "SELECT COUNT(participations.id) "
        "FROM participations "
        "JOIN rounds ON rounds.id=participations.round_id "
        "WHERE participator_id = ?"
    )

    params = [user_id]

    if timeparam:
        if timeparam == FindRoundParam.DATE_NOW_OR_AFTER:
            sql = sql + " AND start_time >= ?"
        elif timeparam == FindRoundParam.DATE_BEFORE:
            sql = sql + " AND start_time <= ?"

        params.insert(1, datetime.datetime.now().isoformat(timespec="minutes"))

    result = db.fetch_one_from_db(sql, params)
    return result[0]


def round_participations_count(round_id):
    sql = "SELECT COUNT(id) FROM participations WHERE round_id = ?"

    result = db.fetch_one_from_db(sql, [round_id])
    return result[0]


def find_participating_rounds(user_id, page, page_size, timeparam):
    params = [user_id]
    params.extend(get_page_limit_and_offset(page, page_size))
    sql = (
        "SELECT rounds.id, coursename, username, start_time, num_players, "
        "IFNULL(COUNT(participations.participator_id) + 1, 1) AS num_participating "
        "FROM rounds "
        "JOIN users ON users.id=rounds.creator_id "
        "LEFT JOIN participations ON participations.round_id=rounds.id "
        "WHERE rounds.id IN (SELECT round_id FROM participations WHERE participations.participator_id = ?) "
    )

    if timeparam:
        if timeparam == FindRoundParam.DATE_NOW_OR_AFTER:
            sql = sql + "AND start_time >= ? "
        elif timeparam == FindRoundParam.DATE_BEFORE:
            sql = sql + "AND start_time <= ? "

        params.insert(1, datetime.datetime.now().isoformat(timespec="minutes"))

    sql = sql + "GROUP BY rounds.id ORDER BY start_time LIMIT ? OFFSET ?"

    result = db.fetch_all_from_db(sql, params, resp_type=db.RespType.DICT)
    return format_rounds(result) if result else result
