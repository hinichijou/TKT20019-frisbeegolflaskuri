import db


def create_result(round_id, player_id, hole, result):
    result_id = find_result(round_id, player_id, hole)

    if result_id:
        sql = "UPDATE rounds SET result = ? WHERE id = ?"
        db.execute(sql, [result, result_id])
    else:
        sql = "INSERT INTO results (round_id, player_id, hole, result) VALUES (?, ?, ?, ?)"
        db.execute(sql, [round_id, player_id, hole, result])


def find_result(round_id, player_id, hole):
    sql = "SELECT id FROM results WHERE round_id=? AND player_id=? AND hole=?"

    result = db.fetch_one_from_db(sql, [round_id, player_id, hole])
    return result[0]
