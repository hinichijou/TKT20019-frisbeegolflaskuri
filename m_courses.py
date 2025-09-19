import json
import db

default_format_options = {"hole_data": True}

def add_course(data):
    sql = "INSERT INTO courses (coursename, num_holes, hole_data) VALUES (?, ?, ?)"
    db.execute(sql, [data["coursename"], data["num_holes"], json.dumps(data["hole_data"])])

    course_id = db.last_insert_id()

    add_course_selection(course_id, data["difficulty_select"][0])
    add_course_selection(course_id, data["type_select"][0])

def add_course_selection(course_id, selection):
    sql = "INSERT INTO course_selections (item_id, course_id) VALUES (?, ?)"
    db.execute(sql, [selection, course_id])

def delete_course(course_id):
    sql = "DELETE FROM course_selections WHERE course_id = ?"
    db.execute(sql, [course_id])
    sql = "DELETE FROM courses WHERE id = ?"
    db.execute(sql, [course_id])

def update_course(data):
    sql = "UPDATE courses SET coursename = ?, num_holes = ?, hole_data = ? WHERE id = ?"
    db.execute(sql, [data["coursename"], data["num_holes"], json.dumps(data["hole_data"]), data["id"]])

    sql = "DELETE FROM course_selections WHERE course_id = ?"
    db.execute(sql, [data["id"]])

    #Currently the classifications for the course are required in course creation and not in course modification
    #This is mainly because I couldn't decide if I should require them or not
    if data["difficulty_select"][0]:
        add_course_selection(data["id"], data["difficulty_select"][0])
    if data["type_select"][0]:
        add_course_selection(data["id"], data["type_select"][0])

def get_courses():
    sql = "SELECT id, coursename, num_holes FROM courses"
    return db.query_db(sql, resp_type = db.RespType.DICT)

def get_course_data(id, format_options = default_format_options):
    sql = "SELECT courses.id, coursename, num_holes, hole_data, " \
            "GROUP_CONCAT(course_selections.item_id) AS item_ids, " \
            "GROUP_CONCAT(selection_class_items.item_key) AS item_keys, " \
            "GROUP_CONCAT(selection_classes.class_key) AS item_class_keys " \
            "FROM courses " \
            "LEFT JOIN course_selections ON course_selections.course_id=courses.id " \
            "LEFT JOIN selection_class_items ON selection_class_items.id=course_selections.item_id " \
            "LEFT JOIN selection_classes ON selection_classes.id=selection_class_items.class_id " \
            "WHERE courses.id = ? " \
            "GROUP BY courses.id "
    result = db.query_db(sql, [id], resp_type = db.RespType.DICT)
    return format_course_data(result, format_options)[0] if result else result

def format_course_data(data, format_options):
    for row in data:
        if  "item_ids" in row and row["item_ids"] and "item_keys" in row and row["item_keys"] and "item_class_keys" in row and row["item_class_keys"]:
            item_ids = row["item_ids"].split(",")
            item_keys = row["item_keys"].split(",")
            item_class_keys = row["item_class_keys"].split(",")
            if len(item_ids) == len(item_keys) == len(item_class_keys):
                row["items"] = {item_class_keys[i]: (int(item_ids[i]), item_keys[i]) for i in range(len(item_ids))}

        if format_options["hole_data"] and "hole_data" in row:
            row["hole_data"] = json.loads(row["hole_data"])

    return data