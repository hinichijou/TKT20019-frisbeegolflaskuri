import db

def add_round(course_id, creator, start_time, num_players):
    sql = "INSERT INTO rounds (course_id, creator_id, start_time, num_players, attendees) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [course_id, creator, start_time, num_players, ""])