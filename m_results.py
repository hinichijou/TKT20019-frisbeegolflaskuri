import db


def create_result(round_id, player_id, hole, result):
    sql = "INSERT INTO results (round_id, player_id, hole, result) VALUES (?, ?, ?, ?)"
    db.execute(sql, [round_id, player_id, hole, result])


def update_result(result_id, result):
    sql = "UPDATE results SET result = ? WHERE id = ?"
    db.execute(sql, [result, result_id])


def find_round_results(round_id):
    sql = (
        "SELECT results.id, player_id, hole, result, username "
        "FROM results "
        "JOIN users ON users.id=results.player_id "
        "WHERE round_id=?"
    )
    result = db.fetch_all_from_db(sql, [round_id], resp_type=db.RespType.DICT)
    return format_round_results(result) if result else result


def format_round_results(results):
    formatted_results = {}
    for row in results:
        user_id = row["player_id"]
        if user_id not in formatted_results:
            formatted_results[user_id] = {}
            formatted_results[user_id]["username"] = row["username"]

        formatted_results[user_id]["total"] = (
            row["result"]
            if "total" not in formatted_results[user_id]
            else formatted_results[user_id]["total"] + row["result"]
        )

        hole = row["hole"]
        formatted_results[user_id][hole] = {}
        formatted_results[user_id][hole]["result_id"] = row["id"]
        formatted_results[user_id][hole]["result"] = row["result"]

    return formatted_results


def find_hole_result(round_id, player_id, hole):
    sql = "SELECT id, result FROM results WHERE round_id=? AND player_id=? AND hole=?"
    result = db.fetch_one_from_db(sql, [round_id, player_id, hole])
    return result


def delete_results_for_round(round_id):
    sql = "DELETE FROM results WHERE round_id = ?"
    db.execute(sql, [round_id])
