import db

def add_course(coursename, num_holes):
    sql = "INSERT INTO courses (coursename, num_holes) VALUES (?, ?)"
    db.execute(sql, [coursename, num_holes])

def get_courses():
    sql = "SELECT id, coursename FROM courses"
    return db.query(sql)