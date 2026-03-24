import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
from datetime import datetime

app = Flask(__name__)
app.secret_key=config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new_event")
def new_event():
    return render_template("new_event.html")

@app.route("/add_event", methods=["POST"])
def add_event():
    event_name=request.form["event_name"]
    date_time=request.form["date_time"]
    date_time= datetime.strptime(date_time, "%Y-%m-%dT%H:%M")
    date_time=date_time.strftime("%Y-%m-%d %H:%M:%S")
    print(date_time)
    description=request.form["description"]
    print(description)
    user_id= session["user_id"]
    if user_id:
        print(user_id)
    else:
        print("user_id not exist")

    sql = "INSERT INTO events (event_name, date_time, description, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [event_name, date_time, description, user_id])

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
        return "ERROR: Passwords are not the same"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "ERROR: Username is already taken"

    return "Username created"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template('login.html')
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result= db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"]= user_id
            session["username"] = username
            return redirect("/")
        else:
            return "ERROR: incorrect username or password"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")
