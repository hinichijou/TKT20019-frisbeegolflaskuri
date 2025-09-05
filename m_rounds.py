import db

def add_round(course_id, creator, start_time, num_players):
    sql = "INSERT INTO rounds (course_id, creator_id, start_time, num_players) VALUES (?, ?, ?, ?)"
    db.execute(sql, [course_id, creator, start_time, num_players])

def get_rounds():
    sql = "SELECT rounds.id, coursename, username, start_time, num_players, IFNULL(SUM(participations.participator_id) + 1, 1) AS num_participating FROM rounds " \
            "JOIN courses ON courses.id=rounds.course_id " \
            "JOIN users ON users.id=rounds.creator_id " \
            "LEFT JOIN participations ON participations.round_id=rounds.id"
    return db.query(sql)