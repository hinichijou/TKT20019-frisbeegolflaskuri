import json
import db
from enums import FindCourseParam
from utilities import use_default_if_list_none, get_page_limit_and_offset, create_where_condition

default_format_options = {"hole_data": True}


def add_course(data):
    sql = "INSERT INTO courses (coursename, num_holes, hole_data) VALUES (?, ?, ?)"
    db.execute(sql, [data["coursename"], data["num_holes"], json.dumps(data["hole_data"])])

    course_id = db.last_insert_id()

    add_course_selection(course_id, data["difficulty_select"][0])
    add_course_selection(course_id, data["type_select"][0])

    return course_id


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

    # Currently the classifications for the course are required in course creation and not in course modification
    # This is mainly because I couldn't decide if I should require them or not
    if data["difficulty_select"][0]:
        add_course_selection(data["id"], data["difficulty_select"][0])
    if data["type_select"][0]:
        add_course_selection(data["id"], data["type_select"][0])


def get_courses(page, page_size):
    sql = "SELECT id, coursename, num_holes FROM courses LIMIT ? OFFSET ?"
    limit, offset = get_page_limit_and_offset(page, page_size)
    return db.fetch_all_from_db(sql, [limit, offset], resp_type=db.RespType.DICT)


def get_sql_for_param(param):
    match param:
        case FindCourseParam.COURSENAME:
            return "coursename LIKE ?"
        case FindCourseParam.NUM_HOLES:
            return "num_holes = ?"
        case FindCourseParam.TYPE:
            return "course_selections.item_id=?"
        case FindCourseParam.DIFFICULTY:
            return "course_selections.item_id=?"
        case _:
            return ""


# Params None returns count of all courses
def courses_count(searchparams=None):
    params = None

    if searchparams:
        types, params = zip(*searchparams)

        has_classifications = FindCourseParam.TYPE in types or FindCourseParam.DIFFICULTY in types
        if has_classifications:
            if FindCourseParam.TYPE in types and FindCourseParam.DIFFICULTY in types:
                sql = (
                    "WITH selections AS ("
                    "SELECT course_id "
                    "FROM course_selections "
                    "WHERE item_id = ? "
                    "INTERSECT "
                    "SELECT course_id "
                    "FROM course_selections "
                    "WHERE item_id = ?) "
                    "SELECT COUNT(courses.id) "
                    "FROM courses "
                    "INNER JOIN selections ON selections.course_id=courses.id"
                )
                types = [t for t in types if t not in (FindCourseParam.TYPE, FindCourseParam.DIFFICULTY)]
            else:
                sql = (
                    "SELECT COUNT(courses.id) "
                    "FROM courses "
                    "LEFT JOIN course_selections ON course_selections.course_id=courses.id"
                )
        else:
            sql = "SELECT COUNT(courses.id) FROM courses"

        where = create_where_condition(types, get_sql_for_param).rstrip()

        if where:
            sql += f" {where}"
    else:
        sql = "SELECT COUNT(courses.id) FROM courses"

    result = db.fetch_one_from_db(sql, params)
    return result[0] if result else 0


def find_courses(searchparams, page, page_size):
    types, params = zip(*searchparams)
    params = params + get_page_limit_and_offset(page, page_size)

    has_classifications = FindCourseParam.TYPE in types or FindCourseParam.DIFFICULTY in types
    if has_classifications:
        if FindCourseParam.TYPE in types and FindCourseParam.DIFFICULTY in types:
            sql = (
                "WITH selections AS ("
                "SELECT course_id "
                "FROM course_selections "
                "WHERE item_id = ? "
                "INTERSECT "
                "SELECT course_id "
                "FROM course_selections "
                "WHERE item_id = ?) "
                "SELECT courses.id, coursename, num_holes "
                "FROM courses "
                "INNER JOIN selections ON selections.course_id=courses.id"
            )
            types = [t for t in types if t not in (FindCourseParam.TYPE, FindCourseParam.DIFFICULTY)]
            where = create_where_condition(types, get_sql_for_param).rstrip()
            sql += " " + where + " LIMIT ? OFFSET ?"
        else:
            where = create_where_condition(types, get_sql_for_param).rstrip()
            sql = (
                "SELECT courses.id, coursename, num_holes "
                "FROM courses "
                "LEFT JOIN course_selections ON course_selections.course_id=courses.id "
                + where
                + " GROUP BY courses.id "
                "LIMIT ? OFFSET ?"
            )
    else:
        where = create_where_condition(types, get_sql_for_param).rstrip()
        sql = "SELECT courses.id, coursename, num_holes FROM courses " + where + " LIMIT ? OFFSET ?"

    return db.fetch_all_from_db(sql, params, resp_type=db.RespType.DICT)


def get_course_data(course_id, format_options=None):
    format_options = use_default_if_list_none(format_options, default=default_format_options)

    sql = (
        "SELECT courses.id, coursename, num_holes, hole_data, "
        "GROUP_CONCAT(course_selections.item_id) AS item_ids, "
        "GROUP_CONCAT(selection_class_items.item_key) AS item_keys, "
        "GROUP_CONCAT(selection_classes.class_key) AS item_class_keys "
        "FROM courses "
        "LEFT JOIN course_selections ON course_selections.course_id=courses.id "
        "LEFT JOIN selection_class_items ON selection_class_items.id=course_selections.item_id "
        "LEFT JOIN selection_classes ON selection_classes.id=selection_class_items.class_id "
        "WHERE courses.id = ? "
        "GROUP BY courses.id "
    )
    result = db.fetch_all_from_db(sql, [course_id], resp_type=db.RespType.DICT)
    return format_course_data(result, format_options)[0] if result else result


item_fields = ["item_ids", "item_keys", "item_class_keys"]


def format_course_data(data, format_options):
    for row in data:
        if all(f in row and row[f] for f in item_fields):
            item_ids = row["item_ids"].split(",")
            item_keys = row["item_keys"].split(",")
            item_class_keys = row["item_class_keys"].split(",")
            if len(item_ids) == len(item_keys) == len(item_class_keys):
                row["items"] = {item_class_keys[i]: (int(item_ids[i]), item_keys[i]) for i in range(len(item_ids))}

        if format_options["hole_data"] and "hole_data" in row:
            row["hole_data"] = json.loads(row["hole_data"])

    return data
