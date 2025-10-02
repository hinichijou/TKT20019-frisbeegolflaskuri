import db


def create_user(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])


def get_user_id_and_hash(username):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query_db(sql, [username])
    return result[0] if result else result


def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query_db(sql, [user_id])
    return result[0] if result else result
