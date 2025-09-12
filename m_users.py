import db

def create_user(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def get_user_id_and_hash(username):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    return db.query_db(sql, [username])

def get_username(id):
    sql = "SELECT username FROM users WHERE id = ?"
    return db.query_db(sql, [id])