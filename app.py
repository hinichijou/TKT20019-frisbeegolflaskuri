import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import config
from constants import constants
import m_users
import m_rounds
import m_courses

app = Flask(__name__)
app.secret_key = config.secret_key

#TODO: Collect strings to own file. Localization support?
str_no_courses_found = "VIRHE: ei ratoja tietokannassa. Luo rata luodaksesi kierroksen."

def require_login():
    if "user_id" not in session:
        abort(403)

def abort_if_id_not_sid(user_id):
    if session["user_id"] != user_id:
        abort(403)

def abort_if_null(obj, abortcode):
    if not obj:
        abort(abortcode)

def test_inputs(input_tests):
    for f in input_tests:
        if not f():
            abort(403)

def test_num(input):
    try:
        int(input)
    except ValueError:
        return False

    return True

def test_date(input):
    try:
        datetime.date.fromisoformat(input)
    except ValueError:
        return False

    return True

def test_minmax_limits(val, min, max):
    return val >= min and val <= max

def test_num_minmax(input, min, max):
    return test_num(input) and test_minmax_limits(int(input), min, max)

def test_username(username):
    return test_minmax_limits(len(username), constants.username_minlength, constants.username_maxlength)

def test_password(password):
    return test_minmax_limits(len(password), constants.password_minlength, constants.password_maxlength)

def test_coursename(coursename):
    return test_minmax_limits(len(coursename), constants.coursename_minlength, constants.coursename_maxlength)

def test_course_id(course_id):
    return test_num(course_id)

def test_round_id(round_id):
    return test_num(round_id)

def test_user_id(user_id):
    return test_num(user_id)

def test_start_time(start_time):
    return test_date(start_time)

def test_num_holes(num_holes):
    return test_num_minmax(num_holes, constants.course_holes_min, constants.course_holes_max)

def test_hole_data(hole_data):
    for v in hole_data.values():
        if not (test_num_minmax(v["par"], constants.hole_par_min, constants.hole_par_max)
            and test_num_minmax(v["length"], constants.hole_length_min, constants.hole_length_max)):
            return False

    return True

def test_num_players(num_players):
    return test_num_minmax(num_players, constants.round_min_players, constants.round_max_players)

@app.route("/")
def index():
    return render_template("index.html", rounds = m_rounds.get_all_rounds())

@app.route("/new_course")
def new_course():
    require_login()
    return render_template("new_course.html", constants = constants)

@app.route("/create_course", methods=["POST"])
def create_course():
    require_login()

    coursename = request.form["coursename"]
    num_holes = request.form["num_holes"]

    test_inputs(
        [
            lambda: test_coursename(coursename),
            lambda: test_num_holes(num_holes)
        ]
    )

    return render_template("new_holes.html", constants = constants, coursename = coursename, num_holes = num_holes)

@app.route("/delete_course/<int:course_id>", methods=["GET", "POST"])
def delete_course(course_id):
    require_login()

    test_inputs([lambda: test_course_id(course_id)])

    if request.method == "GET":
        course = m_courses.get_course_data(course_id)

        abort_if_null(course, 404)

        return render_template("delete_course.html", course = course)

    if request.method == "POST":
        if "remove" in request.form:
            m_courses.delete_course(course_id)
            return redirect("/")

        return redirect("/course/" + str(course_id))

@app.route("/show_courses")
def show_courses():
    require_login()

    courses = m_courses.get_courses()
    if not courses:
        return str_no_courses_found

    return render_template("show_courses.html", courses = courses)

@app.route("/course/<int:course_id>")
def show_course(course_id):
    require_login()
    test_inputs([lambda: test_course_id(course_id)])

    course = m_courses.get_course_data(course_id)

    abort_if_null(course, 404)

    return render_template("show_course.html", course = course)

@app.route("/edit_course/<int:course_id>")
def edit_course(course_id):
    require_login()
    test_inputs([lambda: test_course_id(course_id)])

    course = m_courses.get_course_data(course_id)

    abort_if_null(course, 404)

    return render_template("edit_course_num_holes.html", constants = constants, course = course)

def build_course_data(form):
    hole_data = create_holes_dict(form)

    test_inputs(
        [
            lambda: test_course_id(form["id"]),
            lambda: test_coursename(form["coursename"]),
            lambda: test_num_holes(form["num_holes"]),
            lambda: test_hole_data(hole_data)
        ]
    )

    course = {
        "id": form["id"],
        "coursename": form["coursename"],
        "num_holes": form["num_holes"],
        "hole_data": hole_data
    }

    return course

@app.route("/edit_course_holes", methods=["POST"])
def edit_course_holes():
    require_login()

    course = build_course_data(request.form)

    return render_template("edit_course_holes.html", constants = constants, course = course)

@app.route("/update_course", methods=["POST"])
def update_course():
    require_login()

    course = build_course_data(request.form)
    m_courses.update_course(course)

    return redirect("/course/" + course["id"])

def create_holes_dict(form):
    holes_dict = {}
    for i in range(1, int(form["num_holes"]) + 1):
        parkey = f"par_{i}"
        lengthkey = f"length_{i}"
        # If we are adding holes the data for new holes might not be in the form yet
        if parkey in form and lengthkey in form:
            holes_dict[i] = {"par": form[parkey], "length": form[lengthkey]}
        else:
            break

    return holes_dict

@app.route("/create_holes", methods=["POST"])
def create_holes():
    require_login()

    coursename = request.form["coursename"]
    num_holes = request.form["num_holes"]
    hole_data = create_holes_dict(request.form)

    test_inputs(
        [
            lambda: test_coursename(coursename),
            lambda: test_num_holes(num_holes),
            lambda: test_hole_data(hole_data)
        ]
    )

    m_courses.add_course(coursename, num_holes, hole_data)

    return redirect("/")

@app.route("/new_round")
def new_round():
    require_login()

    courses = m_courses.get_courses()
    if not courses:
        return str_no_courses_found

    return render_template("new_round.html", constants = constants, courses = courses, date = datetime.datetime.now().isoformat(timespec="minutes"))

@app.route("/create_round", methods=["POST"])
def create_round():
    require_login()

    course_id = request.form["course_select"]
    start_time = request.form["start_time"]
    num_players = request.form["num_players"]

    test_inputs(
        [
            lambda: test_course_id(course_id),
            lambda: test_start_time(start_time),
            lambda: test_num_players(num_players)
        ]
    )

    m_rounds.add_round(course_id, session["user_id"], start_time, num_players)

    return redirect("/")

@app.route("/delete_round/<int:round_id>", methods=["GET", "POST"])
def delete_round(round_id):
    require_login()

    test_inputs([lambda: test_round_id(round_id)])

    abort_if_id_not_sid(m_rounds.get_user_id_for_round(round_id))

    if request.method == "GET":
        round = m_rounds.get_round(round_id)

        abort_if_null(round, 404)

        return render_template("delete_round.html", round = round)

    if request.method == "POST":
        if "remove" in request.form:
            m_rounds.delete_round(round_id)
            return redirect("/")

        return redirect("/round/" + str(round_id))

@app.route("/find_round")
def find_round():
    require_login()

    input_tests = []

    course_query = request.args.get("course_select")
    if course_query and course_query != "":
        input_tests.append(lambda: test_coursename(course_query))

    start_time = request.args.get("start_time")
    if start_time and start_time != "":
        input_tests.append(lambda: test_start_time(start_time))

    test_inputs(input_tests)

    arginput = course_query != None or start_time != None

    searchparams = []

    if not course_query:
        course_query = ""
    else:
        #Search course name only if something is set
        searchparams.append((m_rounds.FindRoundParam.COURSENAME, course_query))

    if not start_time:
        start_time = "" # datetime.date.today().isoformat() would set to today
    else:
        #Search date only if something is set
        searchparams.append((m_rounds.FindRoundParam.DATE, start_time + "%"))

    #With default parameters returns all rounds if they are sent in the query
    results = m_rounds.find_rounds(searchparams) if len(searchparams) > 0 else m_rounds.get_all_rounds() if arginput else []

    courses = m_courses.get_courses()
    if not courses:
        courses = []

    return render_template("find_round.html", courses = courses, course_query = course_query, start_time = start_time, results = results, arginput = arginput)

@app.route("/round/<int:round_id>")
def show_round(round_id):
    require_login()
    test_inputs([lambda: test_round_id(round_id)])

    round = m_rounds.get_round(round_id)

    abort_if_null(round, 404)

    return render_template("show_round.html", round = round)

@app.route("/edit_round/<int:round_id>")
def edit_round(round_id):
    require_login()
    test_inputs([lambda: test_round_id(round_id)])

    round = m_rounds.get_round(round_id, {"start_time": False, "hole_data": True})

    abort_if_null(round, 404)
    abort_if_id_not_sid(m_rounds.get_user_id_for_round(round["id"]))

    courses = m_courses.get_courses()
    if not courses:
        courses = []

    for i in range(len(courses)):
        if courses[i]["coursename"] == round["coursename"]:
            del courses[i]
            break

    return render_template("edit_round.html", constants = constants, courses = courses, round = round)

def build_round_data_course_select(form):
    test_inputs(
        [
            lambda: test_round_id(form["id"]),
            lambda: test_course_id(form["course_select"]),
            lambda: test_start_time(form["start_time"]),
            lambda: test_num_players(form["num_players"])
        ]
    )

    round = {
        "id": form["id"],
        "start_time": form["start_time"],
        "num_players": form["num_players"],
        "course_id": form["course_select"]
    }

    #In this case the user didn't change the course selection
    if round["course_id"] == "":
        hole_data = create_holes_dict(form)
        test_inputs(
            [
                lambda: test_coursename(form["coursename"]),
                lambda: test_num_holes(form["num_holes"]),
                lambda: test_hole_data(hole_data)
            ]
        )
        round["coursename"] = form["coursename"]
        round["num_holes"] = form["num_holes"]
        round["hole_data"] = hole_data
    #The user did change the course selection. Update the course information from db
    else:
        course_data = m_courses.get_course_data(round["course_id"])
        round["coursename"] = course_data["coursename"]
        round["num_holes"] = course_data["num_holes"]
        round["hole_data"] = course_data["hole_data"]

    return round

def get_round_user_id(round):
    round["user_id"] = m_rounds.get_user_id_for_round(round["id"])
    abort_if_id_not_sid(round["user_id"])

@app.route("/update_round_basic", methods=["POST"])
def update_round_basic():
    require_login()

    round = build_round_data_course_select(request.form)
    get_round_user_id(round)
    m_rounds.update_round(round)
    return redirect("/round/" + round["id"])

@app.route("/edit_round_num_holes", methods=["POST"])
def edit_round_num_holes():
    require_login()

    round = build_round_data_course_select(request.form)
    get_round_user_id(round)
    return render_template("edit_round_num_holes.html", constants = constants, round = round)

def build_round_data(form):
    hole_data = create_holes_dict(form)

    test_inputs(
        [
            lambda: test_round_id(form["id"]),
            lambda: test_coursename(form["coursename"]),
            lambda: test_start_time(form["start_time"]),
            lambda: test_num_players(form["num_players"]),
            lambda: test_num_holes(form["num_holes"]),
            lambda: test_hole_data(hole_data)
        ]
    )

    round = {
        "id": form["id"],
        "start_time": form["start_time"],
        "num_players": form["num_players"],
        "coursename": form["coursename"],
        "num_holes": form["num_holes"],
        "hole_data": hole_data
    }

    return round

@app.route("/edit_round_holes", methods=["POST"])
def edit_round_holes():
    require_login()

    round = build_round_data(request.form)
    get_round_user_id(round)
    return render_template("edit_round_holes.html", constants = constants, round = round)

@app.route("/update_round_full", methods=["POST"])
def update_round_full():
    require_login()

    round = build_round_data(request.form)
    get_round_user_id(round)
    m_rounds.update_round(round)

    return redirect("/round/" + round["id"])

@app.route("/user/<int:user_id>")
def show_user(user_id):
    require_login()
    test_inputs([lambda: test_user_id(user_id)])

    user = m_users.get_user(user_id)
    rounds = m_rounds.find_rounds([(m_rounds.FindRoundParam.CREATORID, user_id)])

    abort_if_null(user, 404)

    return render_template("show_user.html", user = user, rounds = rounds)

@app.route("/register")
def register():
    return render_template("register.html", constants = constants)

@app.route("/registered")
def registered():
    return render_template("registered.html")

@app.route("/create", methods=["POST"])
def create():
    test_inputs(
        [
            lambda: test_username(request.form["username"]),
            lambda: test_password(request.form["password1"]),
            lambda: test_password(request.form["password2"]),
        ]
    )

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    try:
        m_users.create_user(username, generate_password_hash(password1))
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return redirect("/registered")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", constants = constants)
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
            return "VIRHE: käyttäjää ei ole olemassa"

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    require_login()

    del session["username"]
    del session["user_id"]
    return redirect("/")
