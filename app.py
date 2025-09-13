import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import config
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

@app.route("/")
def index():
    return render_template("index.html", rounds = m_rounds.get_all_rounds())

@app.route("/new_course")
def new_course():
    require_login()
    return render_template("new_course.html")

@app.route("/create_course", methods=["POST"])
def create_course():
    require_login()

    coursename = request.form["coursename"]
    num_holes = request.form["num_holes"]

    return render_template("new_holes.html", coursename = coursename, num_holes = num_holes)

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

    m_courses.add_course(coursename, num_holes, create_holes_dict(request.form))

    return redirect("/")

@app.route("/new_round")
def new_round():
    require_login()

    courses = m_courses.get_courses()

    if not courses:
        return str_no_courses_found

    return render_template("new_round.html", courses = courses, date = datetime.datetime.now().isoformat(timespec="minutes"))

@app.route("/create_round", methods=["POST"])
def create_round():
    require_login()

    course_id = request.form["course_select"]
    start_time = request.form["start_time"]
    num_players = request.form["num_players"]

    m_rounds.add_round(course_id, session["user_id"], start_time, num_players)

    return redirect("/")

@app.route("/delete_round/<int:round_id>", methods=["GET", "POST"])
def delete_round(round_id):
    require_login()
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

    courses = m_courses.get_courses()

    course_query = request.args.get("course_select")
    if not course_query:
        course_query = ""
    start_time = request.args.get("start_time")
    if not start_time:
        start_time = datetime.date.today().isoformat()

    results = m_rounds.find_rounds(course_query, start_time)

    return render_template("find_round.html", courses = courses, course_query = course_query, start_time = start_time, results = results)

@app.route("/round/<int:round_id>")
def show_round(round_id):
    require_login()

    round = m_rounds.get_round(round_id)

    abort_if_null(round, 404)

    return render_template("show_round.html", round = round)

@app.route("/edit_round/<int:round_id>")
def edit_round(round_id):
    require_login()

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

    return render_template("edit_round.html", courses = courses, round = round)

def build_round_data_course_select(form):
    round = {
        "id": form["id"],
        "start_time": form["start_time"],
        "num_players": form["num_players"],
        "course_id": form["course_select"]
    }

    #In this case the user didn't change the course selection
    if round["course_id"] == "":
        round["coursename"] = form["coursename"]
        round["num_holes"] = form["num_holes"]
        round["hole_data"] = create_holes_dict(form)
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
    return render_template("edit_round_num_holes.html", round = round)

def build_round_data(form):
    round = {
        "id": form["id"],
        "start_time": form["start_time"],
        "num_players": form["num_players"],
        "coursename": form["coursename"],
        "num_holes": form["num_holes"],
        "hole_data": create_holes_dict(form)
    }

    return round

@app.route("/edit_round_holes", methods=["POST"])
def edit_round_holes():
    require_login()

    round = build_round_data(request.form)
    get_round_user_id(round)
    return render_template("edit_round_holes.html", round = round)

@app.route("/update_round_full", methods=["POST"])
def update_round_full():
    require_login()

    round = build_round_data(request.form)
    get_round_user_id(round)
    m_rounds.update_round(round)

    return redirect("/round/" + round["id"])

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    try:
        m_users.create_user(username, generate_password_hash(password1))
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        result = m_users.get_user_id_and_hash(username)

        if result:
            user_id = result[0]["id"]
            password_hash = result[0]["password_hash"]
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
