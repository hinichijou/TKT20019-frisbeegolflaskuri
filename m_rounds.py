import db

def add_round(course_id, creator, start_time, num_players):
    sql = "INSERT INTO rounds (course_id, creator_id, start_time, num_players) VALUES (?, ?, ?, ?)"
    db.execute(sql, [course_id, creator, start_time, num_players])

def get_rounds():
    sql = "SELECT id, coursename FROM courses"
    return db.query(sql)