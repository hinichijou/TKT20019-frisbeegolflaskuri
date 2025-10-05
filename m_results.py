import db


def create_result(round_id, player_id, hole, result):
    sql = "INSERT INTO results (round_id, player_id, hole, result) VALUES (?, ?, ?, ?)"
    db.execute(sql, [round_id, player_id, hole, result])


def update_result(result_id, result):
    sql = "UPDATE results SET result = ? WHERE id = ?"
    db.execute(sql, [result, result_id])


def find_result(round_id, player_id, hole):
    sql = "SELECT id, result FROM results WHERE round_id=? AND player_id=? AND hole=?"
    result = db.fetch_one_from_db(sql, [round_id, player_id, hole])
    return result
