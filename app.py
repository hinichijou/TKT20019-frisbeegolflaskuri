import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import datetime

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new_course")
def new_course():
    return render_template("new_course.html")

@app.route("/create_course", methods=["POST"])
def create_course():
    coursename = request.form["coursename"]
    num_holes = request.form["num_holes"]

    sql = "INSERT INTO courses (coursename, num_holes) VALUES (?, ?)"
    db.execute(sql, [coursename, num_holes])

    return redirect("/")

@app.route("/new_round")
def new_round():
    sql = "SELECT id, coursename FROM courses"
    result = db.query(sql)

    if result:
        courses = result
    else:
        return "VIRHE: ei ratoja tietokannassa. Luo rata luodaksesi kierroksen."

    return render_template("new_round.html", courses = courses, date = datetime.datetime.now().isoformat(timespec="minutes"))

@app.route("/create_round", methods=["POST"])
def create_round():
    course_id = request.form["course_select"]
    start_time = request.form["start_time"]
    num_players = request.form["num_players"]
    attendees = ""

    sql = "INSERT INTO rounds (course_id, creator_id, start_time, num_players, attendees) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [course_id, session["user_id"], start_time, num_players, attendees])

    return redirect("/")

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
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
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

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])

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
    del session["username"]
    del session["user_id"]
    return redirect("/")
