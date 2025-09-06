import json
import db

def add_course(coursename, num_holes, holes_dict):
    holes = json.dumps(holes_dict)
    sql = "INSERT INTO courses (coursename, num_holes, holes) VALUES (?, ?, ?)"
    db.execute(sql, [coursename, num_holes, holes])

def get_courses():
    sql = "SELECT id, coursename FROM courses"
    return db.query(sql)

def get_coursename(id):
    sql = "SELECT coursename FROM courses WHERE id = ?"
    result = db.query(sql, [id])
    return result[0] if result else result

def get_course_data_dict(id):
    sql = "SELECT coursename, num_holes, holes FROM courses WHERE id = ?"
    result = db.query_dict(sql, [id])
    return result[0] if result else result