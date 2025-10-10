import math
import secrets
import sqlite3
import time
import datetime

from flask import Flask
from flask import abort, redirect, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash

import config
from constants import constants
from enums import SelectionItemClass, FindRoundParam, FlashCategory
from localizationkeys import LocalizationKeys
from localization import get_localization
import utilities
import m_users
import m_rounds
import m_courses
import m_selection_classes
import m_results

app = Flask(__name__)
app.secret_key = config.secret_key


@app.context_processor
def utility_processor():
    return {"get_localization": get_localization, "constants": constants, "utilities": utilities}


@app.before_request
def before_request():
    g.start_time = time.time()


@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response


def show_message_and_redirect(key, category, route):
    flash(get_localization(key), category)
    return redirect(route)


def show_success_and_redirect(key, route):
    return show_message_and_redirect(key, FlashCategory.MESSAGE, route)


def show_error_and_redirect(key, route):
    return show_message_and_redirect(key, FlashCategory.ERROR, route)


def require_login():
    if "user_id" not in session:
        abort(403)


def check_csrf(form):
    if "csrf_token" not in form or form["csrf_token"] != session["csrf_token"]:
        abort(403)


def abort_if_id_not_sid(user_id):
    if session["user_id"] != user_id:
        abort(403)


def abort_if_sid_not_in_list(id_list):
    if session["user_id"] not in id_list:
        abort(403)


def abort_if_null(obj, abortcode):
    if not obj:
        abort(abortcode)


def abort_if_not_in_selections(course, allow_empty=False):
    selections = m_selection_classes.get_selection_items(
        [SelectionItemClass.COURSE_DIFFICULTY, SelectionItemClass.COURSE_TYPE]
    )

    # Test that the values from form exist in selections
    if (
        course["difficulty_select"][0]
        and (int(course["difficulty_select"][0]), course["difficulty_select"][1]) not in selections["course_difficulty"]
    ):
        abort(403)
    elif not course["difficulty_select"][0] and not allow_empty:
        abort(403)

    if (
        course["type_select"][0]
        and (int(course["type_select"][0]), course["type_select"][1]) not in selections["course_type"]
    ):
        abort(403)
    elif not course["type_select"][0] and not allow_empty:
        abort(403)


def test_inputs(input_tests):
    for f in input_tests:
        if not f():
            abort(403)


def test_num(num):
    try:
        int(num)
    except ValueError:
        return False

    return True


def test_date(date):
    try:
        datetime.datetime.fromisoformat(date)
    except ValueError:
        return False

    return True


def test_minmax_limits(val, min_val, max_val):
    return min_val <= val <= max_val


def test_num_minmax(num, min_val, max_val):
    return test_num(num) and test_minmax_limits(int(num), min_val, max_val)


def test_username(username):
    return test_minmax_limits(len(username), constants.username_minlength, constants.username_maxlength)


def test_password(password):
    return test_minmax_limits(len(password), constants.password_minlength, constants.password_maxlength)


def test_coursename(coursename):
    return test_minmax_limits(len(coursename), constants.coursename_minlength, constants.coursename_maxlength)


def test_course_id(course_id, allow_empty=False):
    return test_num(course_id) or (allow_empty and course_id == "")


def test_round_id(round_id):
    return test_num(round_id)


def test_user_id(user_id):
    return test_num(user_id)


def test_page(page):
    return test_num(page)


def test_hole_num(hole):
    return test_num(hole)


def test_hole_result(result):
    return test_num(result)


def test_start_time(start_time):
    return test_date(start_time)


def test_num_holes(num_holes):
    return test_num_minmax(num_holes, constants.course_holes_min, constants.course_holes_max)


def test_hole_data(hole_data):
    for i in range(len(hole_data.keys())):
        if str(i + 1) not in hole_data.keys():
            return False

    for v in hole_data.values():
        if not (
            test_num_minmax(v["par"], constants.hole_par_min, constants.hole_par_max)
            and test_num_minmax(v["length"], constants.hole_length_min, constants.hole_length_max)
        ):
            return False

    return True


def test_num_players(num_players):
    return test_num_minmax(num_players, constants.round_min_players, constants.round_max_players)


def list_from_form_comma_string(t):
    return t.split(",")


def test_item_id(item, allow_empty_input):
    item_split = list_from_form_comma_string(item)

    return (
        len(item_split) == 2 and test_num(item_split[0])
        if not allow_empty_input
        else (len(item_split) == 2 and test_num(item_split[0])) or item == ""
    )


def format_selections_to_list(course):
    course["type_select"] = list_from_form_comma_string(course["type_select"])
    course["difficulty_select"] = list_from_form_comma_string(course["difficulty_select"])


def get_page_size_and_count(content_count):
    page_size = constants.page_size
    page_count = math.ceil(content_count / page_size)
    page_count = max(page_count, 1)

    return page_size, page_count


def render_page_if_in_page_limits(page, page_count, path, page_func):
    if page < 1:
        return redirect(path + "1")
    if page > page_count:
        return redirect(path + str(page_count))

    return page_func()


@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    input_tests = [lambda: test_page(page)]
    test_inputs(input_tests)

    # Don't query rounds if user not logged in since they are only visible for logged in viewers.
    # Would make more sense to have separate pages before and after login
    if "user_id" in session:
        page_size, page_count = get_page_size_and_count(m_rounds.round_count())
        rounds = m_rounds.get_all_rounds(page, page_size)
    else:
        page_size = 1
        page_count = 1
        rounds = []

    return render_page_if_in_page_limits(
        page,
        page_count,
        "/",
        lambda: render_template("index.html", page=page, page_count=page_count, rounds=rounds),
    )


@app.route("/new_course")
def new_course():
    require_login()

    selections = m_selection_classes.get_selection_items(
        [SelectionItemClass.COURSE_DIFFICULTY, SelectionItemClass.COURSE_TYPE]
    )

    return render_template("new_course.html", selections=selections)


def get_basic_course_data(form):
    course = {
        "coursename": form["coursename"],
        "num_holes": form["num_holes"],
        "type_select": form["type_select"],
        "difficulty_select": form["difficulty_select"],
    }

    return course


def get_basic_course_data_input_tests(course, allow_empty_item_id=False):
    return [
        lambda: test_coursename(course["coursename"]),
        lambda: test_num_holes(course["num_holes"]),
        lambda: test_item_id(course["type_select"], allow_empty_item_id),
        lambda: test_item_id(course["difficulty_select"], allow_empty_item_id),
    ]


@app.route("/create_course", methods=["POST"])
def create_course():
    require_login()
    check_csrf(request.form)

    course = get_basic_course_data(request.form)

    test_inputs(get_basic_course_data_input_tests(course))

    format_selections_to_list(course)

    return render_template("new_holes.html", course=course)


def create_holes_dict(form):
    holes_dict = {}
    for i in range(1, int(form["num_holes"]) + 1):
        parkey = f"par_{i}"
        lengthkey = f"length_{i}"
        # If we are adding holes the data for new holes might not be in the form yet
        if parkey in form and lengthkey in form:
            holes_dict[str(i)] = {"par": form[parkey], "length": form[lengthkey]}
        else:
            break

    return holes_dict


@app.route("/create_holes", methods=["POST"])
def create_holes():
    require_login()
    check_csrf(request.form)

    course = get_basic_course_data(request.form)
    course["hole_data"] = create_holes_dict(request.form)

    input_tests = get_basic_course_data_input_tests(course)
    input_tests.append(lambda: test_hole_data(course["hole_data"]))
    test_inputs(input_tests)

    format_selections_to_list(course)

    abort_if_not_in_selections(course)

    course_id = m_courses.add_course(course)

    if course_id:
        return show_success_and_redirect(LocalizationKeys.create_course_success, "/course/" + str(course_id))
    else:
        return show_error_and_redirect(LocalizationKeys.create_course_unsuccessful, "/")


@app.route("/delete_course/<int:course_id>", methods=["GET", "POST"])
def delete_course(course_id):
    require_login()

    test_inputs([lambda: test_course_id(course_id)])

    if request.method == "GET":
        course = m_courses.get_course_data(course_id)

        abort_if_null(course, 404)

        return render_template("delete_course.html", course=course)

    if request.method == "POST":
        if "remove" in request.form:
            check_csrf(request.form)
            m_courses.delete_course(course_id)
            return show_success_and_redirect(LocalizationKeys.delete_course_success, "/")

        return redirect("/course/" + str(course_id))


@app.route("/show_courses")
@app.route("/show_courses/<int:page>")
def show_courses(page=1):
    require_login()

    input_tests = [lambda: test_page(page)]
    test_inputs(input_tests)

    page_size, page_count = get_page_size_and_count(m_courses.courses_count())
    courses = m_courses.get_courses(page, page_size)
    if not courses:
        return show_error_and_redirect(LocalizationKeys.no_courses_found, "/")

    return render_template("show_courses.html", page=page, page_count=page_count, courses=courses)


@app.route("/course/<int:course_id>")
def show_course(course_id):
    require_login()
    test_inputs([lambda: test_course_id(course_id)])

    course = m_courses.get_course_data(course_id)

    abort_if_null(course, 404)

    return render_template("show_course.html", course=course)


@app.route("/edit_course/<int:course_id>")
def edit_course(course_id):
    require_login()
    test_inputs([lambda: test_course_id(course_id)])

    course = m_courses.get_course_data(course_id)

    abort_if_null(course, 404)

    selections = m_selection_classes.get_selection_items(
        [SelectionItemClass.COURSE_DIFFICULTY, SelectionItemClass.COURSE_TYPE]
    )

    # Delete the current selection from the possible selections before passing to the template.
    # It will be the default choice based on course data.
    if "items" in course:
        for i in range(len(selections["course_difficulty"])):
            if (
                "course_difficulty" in course["items"]
                and selections["course_difficulty"][i][0] == course["items"]["course_difficulty"][0]
            ):
                del selections["course_difficulty"][i]
                break
        for i in range(len(selections["course_type"])):
            if (
                "course_type" in course["items"]
                and selections["course_type"][i][0] == course["items"]["course_type"][0]
            ):
                del selections["course_type"][i]
                break

    return render_template("edit_course.html", course=course, selections=selections)


def build_course_data(form):
    course = get_basic_course_data(request.form)
    course["id"] = form["id"]
    course["hole_data"] = create_holes_dict(request.form)

    input_tests = get_basic_course_data_input_tests(course, True)
    input_tests.append(lambda: test_course_id(form["id"]))
    input_tests.append(lambda: test_hole_data(course["hole_data"]))
    test_inputs(input_tests)

    format_selections_to_list(course)

    return course


@app.route("/edit_course_holes", methods=["POST"])
def edit_course_holes():
    require_login()
    check_csrf(request.form)

    course = build_course_data(request.form)

    return render_template("edit_course_holes.html", course=course)


@app.route("/update_course", methods=["POST"])
def update_course():
    require_login()
    check_csrf(request.form)

    course = build_course_data(request.form)

    abort_if_not_in_selections(course, True)

    m_courses.update_course(course)

    return redirect("/course/" + course["id"])


@app.route("/new_round")
def new_round():
    require_login()

    courses = m_courses.get_courses(1, m_courses.courses_count())
    if not courses:
        return show_error_and_redirect(LocalizationKeys.no_courses_found, "/")

    return render_template(
        "new_round.html",
        courses=courses,
        date=datetime.datetime.now().isoformat(timespec="minutes"),
    )


@app.route("/create_round", methods=["POST"])
def create_round():
    require_login()
    check_csrf(request.form)

    course_id = request.form["course_select"]
    start_time = request.form["start_time"]
    num_players = request.form["num_players"]

    test_inputs(
        [lambda: test_course_id(course_id), lambda: test_start_time(start_time), lambda: test_num_players(num_players)]
    )

    round_id = m_rounds.add_round(course_id, session["user_id"], start_time, num_players)

    if round_id:
        return show_success_and_redirect(LocalizationKeys.create_round_success, "/round/" + str(round_id))
    else:
        return show_error_and_redirect(LocalizationKeys.create_round_course_does_not_exist, "/")


@app.route("/delete_round/<int:round_id>", methods=["GET", "POST"])
def delete_round(round_id):
    require_login()

    test_inputs([lambda: test_round_id(round_id)])

    abort_if_id_not_sid(m_rounds.get_user_id_for_round(round_id))

    if request.method == "GET":
        round_ = m_rounds.get_round(round_id)

        abort_if_null(round_, 404)

        return render_template("delete_round.html", round=round_)

    if request.method == "POST":
        if "remove" in request.form:
            check_csrf(request.form)
            m_rounds.delete_round(round_id)
            return show_success_and_redirect(LocalizationKeys.delete_round_success, "/")

        return redirect("/round/" + str(round_id))


@app.route("/find_round")
@app.route("/find_round/<int:page>")
def find_round(page=1):
    require_login()

    input_tests = [lambda: test_page(page)]

    course_query = request.args.get("course_select")
    if course_query and course_query != "":
        input_tests.append(lambda: test_coursename(course_query))

    start_time = request.args.get("start_time")
    if start_time and start_time != "":
        input_tests.append(lambda: test_start_time(start_time))

    test_inputs(input_tests)

    arginput = course_query is not None or start_time is not None

    searchparams = []

    if not course_query:
        course_query = ""
    else:
        # Search course name only if something is set
        searchparams.append((FindRoundParam.COURSENAME, course_query))

    if not start_time:
        start_time = ""  # datetime.date.today().isoformat() would set to today
    else:
        # Search date only if something is set
        searchparams.append((FindRoundParam.DATE, start_time + "%"))

    # With default parameters returns all rounds if they are sent in the query
    if len(searchparams) > 0:
        page_size, page_count = get_page_size_and_count(m_rounds.round_count(searchparams))
        results = m_rounds.find_rounds(searchparams, page, page_size)
    elif arginput:
        page_size, page_count = get_page_size_and_count(m_rounds.round_count())
        results = m_rounds.get_all_rounds(page, page_size)
    else:
        page_count = 1
        results = []

    courses = m_courses.get_courses(1, m_courses.courses_count())
    if not courses:
        courses = []

    return render_page_if_in_page_limits(
        page,
        page_count,
        "/find_round/",
        lambda: render_template(
            "find_round.html",
            page=page,
            page_count=page_count,
            courses=courses,
            course_query=course_query,
            start_time=start_time,
            results=results,
            arginput=arginput,
        ),
    )


def round_id_input_handling(round_id):
    test_inputs([lambda: test_round_id(round_id)])

    round_ = m_rounds.get_round(round_id)
    abort_if_null(round_, 404)

    return round_


@app.route("/round/<int:round_id>")
def show_round(round_id):
    require_login()

    round_ = round_id_input_handling(round_id)

    return render_template("show_round.html", round=round_)


@app.route("/edit_round/<int:round_id>")
def edit_round(round_id):
    require_login()
    test_inputs([lambda: test_round_id(round_id)])

    round_ = m_rounds.get_round(round_id)

    abort_if_null(round_, 404)
    abort_if_id_not_sid(round_["creator_id"])

    courses = m_courses.get_courses(1, m_courses.courses_count())
    if not courses:
        courses = []

    # Delete the current selection from the possible selections before passing to the template.
    # It will be the default choice based on round data.
    for i in range(len(courses)):
        if courses[i]["coursename"] == round_["coursename"]:
            del courses[i]
            break

    return render_template("edit_round.html", courses=courses, round=round_)


def build_round_data_course_select(form):
    test_inputs(
        [
            lambda: test_round_id(form["id"]),
            lambda: test_course_id(form["course_select"], True),
            lambda: test_start_time(form["start_time"]),
            lambda: test_num_players(form["num_players"]),
        ]
    )

    round_ = {
        "id": form["id"],
        "start_time": form["start_time"],
        "num_players": form["num_players"],
        "course_id": form["course_select"],
    }

    # In this case the user didn't change the course selection
    if round_["course_id"] == "":
        hole_data = create_holes_dict(form)
        test_inputs(
            [
                lambda: test_coursename(form["coursename"]),
                lambda: test_num_holes(form["num_holes"]),
                lambda: test_hole_data(hole_data),
            ]
        )
        round_["coursename"] = form["coursename"]
        round_["num_holes"] = form["num_holes"]
        round_["hole_data"] = hole_data
    # The user did change the course selection. Update the course information from db
    else:
        course_data = m_courses.get_course_data(round_["course_id"])
        round_["coursename"] = course_data["coursename"]
        round_["num_holes"] = course_data["num_holes"]
        round_["hole_data"] = course_data["hole_data"]

    return round_


def get_round_user_id(round_):
    round_["user_id"] = m_rounds.get_user_id_for_round(round_["id"])
    abort_if_id_not_sid(round_["user_id"])


@app.route("/update_round_basic", methods=["POST"])
def update_round_basic():
    require_login()
    check_csrf(request.form)

    round_ = build_round_data_course_select(request.form)
    get_round_user_id(round_)
    m_rounds.update_round(round_)
    return redirect("/round/" + round_["id"])


@app.route("/edit_round_num_holes", methods=["POST"])
def edit_round_num_holes():
    require_login()
    check_csrf(request.form)

    round_ = build_round_data_course_select(request.form)
    get_round_user_id(round_)
    return render_template("edit_round_num_holes.html", round=round_)


def build_round_data(form):
    hole_data = create_holes_dict(form)

    test_inputs(
        [
            lambda: test_round_id(form["id"]),
            lambda: test_coursename(form["coursename"]),
            lambda: test_start_time(form["start_time"]),
            lambda: test_num_players(form["num_players"]),
            lambda: test_num_holes(form["num_holes"]),
            lambda: test_hole_data(hole_data),
        ]
    )

    round_ = {
        "id": form["id"],
        "start_time": form["start_time"],
        "num_players": form["num_players"],
        "coursename": form["coursename"],
        "num_holes": form["num_holes"],
        "hole_data": hole_data,
    }

    return round_


@app.route("/edit_round_holes", methods=["POST"])
def edit_round_holes():
    require_login()
    check_csrf(request.form)

    round_ = build_round_data(request.form)
    get_round_user_id(round_)
    return render_template("edit_round_holes.html", round=round_)


@app.route("/update_round_full", methods=["POST"])
def update_round_full():
    require_login()
    check_csrf(request.form)

    round_ = build_round_data(request.form)
    get_round_user_id(round_)
    m_rounds.update_round(round_)

    return redirect("/round/" + round_["id"])


@app.route("/user/<int:user_id>")
@app.route("/user/<int:user_id>/<int:r_page>/<int:p_page>")
def show_user(user_id, r_page=1, p_page=1):
    require_login()
    test_inputs([lambda: test_user_id(user_id), lambda: test_page(r_page), lambda: test_page(p_page)])

    user = m_users.get_user(user_id)

    abort_if_null(user, 404)

    # The queries below could be combined to a single query but this is good enough for the time being
    searchparams = [(FindRoundParam.CREATORID, user_id)]
    r_count = m_rounds.round_count(searchparams)
    r_page_size, r_page_count = get_page_size_and_count(r_count)
    rounds = m_rounds.find_rounds(searchparams, r_page, r_page_size)

    p_count = m_rounds.user_participations_count(user_id)
    p_page_size, p_page_count = get_page_size_and_count(p_count)
    participating_rounds = m_rounds.find_participating_rounds(user_id, p_page, p_page_size)

    return render_template(
        "show_user.html",
        user=user,
        rounds=rounds,
        participating_rounds=participating_rounds,
        r_page=r_page,
        r_page_count=r_page_count,
        r_count=r_count,
        p_page=p_page,
        p_page_count=p_page_count,
        p_count=p_count,
    )


@app.route("/round_sign_up", methods=["POST"])
def round_sign_up():
    require_login()
    check_csrf(request.form)

    round_ = round_id_input_handling(request.form["round_id"])

    # Creator is always participating to the round by default.
    # Also check that the participation doesn't exceed the amount set for the round.
    if round_["creator_id"] == session["user_id"] or len(round_["participators"].keys()) >= round_["num_players"]:
        abort(403)

    m_rounds.add_participation(round_["round_id"], session["user_id"])

    return redirect(f"/round/{round_['round_id']}")


@app.route("/round_unparticipate", methods=["POST"])
def round_unparticipate():
    require_login()
    check_csrf(request.form)

    round_ = round_id_input_handling(request.form["round_id"])

    abort_if_sid_not_in_list(round_["participators"].keys())

    m_rounds.delete_participation(round_["round_id"], session["user_id"])

    return redirect(f"/round/{round_['round_id']}")


@app.route("/hole/<int:round_id>/<int:player_id>/<int:hole_num>", methods=["GET", "POST"])
def show_hole(round_id, player_id, hole_num):
    require_login()

    test_inputs([lambda: test_hole_num(hole_num), lambda: test_user_id(player_id)])
    round_ = round_id_input_handling(round_id)

    if 0 >= hole_num or hole_num > int(round_["num_holes"]):
        abort(403)

    player = m_users.get_user(player_id)
    abort_if_null(player, 404)

    # Confirm user has access rights to this round
    if player_id not in round_["participators"].keys():
        abort(403)

    # Check if user already has a result for this hole
    result = m_results.find_result(round_id, player_id, hole_num)
    result = result[1] if result else round_["hole_data"][str(hole_num)]["par"] if str(hole_num) in round_["hole_data"] else constants.hole_par_default

    if request.method == "POST":
        check_csrf(request.form)
        if "result" in request.form:
            test_inputs(
                [lambda: test_hole_result(request.form["result"]), lambda: test_hole_num(request.form["result_hole"])]
            )
            post_result = int(request.form["result"])
            result_hole = int(request.form["result_hole"])

            # Check that the posted hole exists for the round
            if 0 >= result_hole or result_hole > int(round_["num_holes"]):
                abort(403)

            # Check if user already has a result for the posted hole
            prev_result = m_results.find_result(round_id, player_id, result_hole)

            if prev_result:
                # Check that there is a difference in the new posted result
                if prev_result[1] != post_result:
                    m_results.update_result(prev_result[0], post_result)
            else:
                m_results.create_result(round_id, player_id, result_hole, post_result)

            # The end of the course results flow
            if result_hole == round_["num_holes"]:
                return redirect(f"/round/{round_['round_id']}")

    return render_template("show_hole.html", round=round_, player=player, hole_num=hole_num, result=result)


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/registered")
def registered():
    return render_template("registered.html")


@app.route("/create", methods=["POST"])
def create():
    test_inputs(
        [
            lambda: test_username(request.form["username"]),
            lambda: test_password(request.form["password"]),
            lambda: test_password(request.form["repeat_password"]),
        ]
    )

    username = request.form["username"]
    password = request.form["password"]
    repeat_password = request.form["repeat_password"]
    if password != repeat_password:
        return show_error_and_redirect(LocalizationKeys.password_mismatch, "/register")

    try:
        m_users.create_user(username, generate_password_hash(password))
    except sqlite3.IntegrityError:
        return show_error_and_redirect(LocalizationKeys.username_taken, "/register")

    return show_success_and_redirect(LocalizationKeys.registration_success, "/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        test_inputs(
            [
                lambda: test_username(request.form["username"]),
                lambda: test_password(request.form["password"]),
            ]
        )

        username = request.form["username"]
        password = request.form["password"]

        result = m_users.get_user_id_and_hash(username)

        if result:
            user_id = result["id"]
            password_hash = result["password_hash"]
        else:
            return show_error_and_redirect(LocalizationKeys.user_does_not_exist, "/login")

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return show_success_and_redirect(LocalizationKeys.login_success, "/")
        else:
            return show_error_and_redirect(LocalizationKeys.wrong_username_or_password, "/login")


@app.route("/logout")
def logout():
    require_login()

    del session["username"]
    del session["user_id"]
    return show_success_and_redirect(LocalizationKeys.logout_success, "/")
