import json
import db

default_format_options = {"hole_data": True}

def add_course(coursename, num_holes, holes_dict):
    hole_data = json.dumps(holes_dict)
    sql = "INSERT INTO courses (coursename, num_holes, hole_data) VALUES (?, ?, ?)"
    db.execute(sql, [coursename, num_holes, hole_data])

def get_courses():
    sql = "SELECT id, coursename FROM courses"
    return db.query_db(sql, resp_type = db.RespType.DICT)

def get_coursename(id):
    sql = "SELECT coursename FROM courses WHERE id = ?"
    result = db.query_db(sql, [id])
    return result[0] if result else result

def get_course_data(id, format_options = default_format_options):
    sql = "SELECT coursename, num_holes, hole_data FROM courses WHERE id = ?"
    result = db.query_db(sql, [id], resp_type = db.RespType.DICT)
    return format_course_data(result, format_options)[0] if result else result

def format_course_data(data, format_options):
    for row in data:
        if format_options["hole_data"] and "hole_data" in row:
            row["hole_data"] = json.loads(row["hole_data"])

    return data