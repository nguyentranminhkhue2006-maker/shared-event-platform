import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import db
import config
import events

app = Flask(__name__)
app.secret_key=config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_events= events.get_events()
    return render_template("index.html", events=all_events)

@app.route("/find_event")
def find_event():
    query=request.args.get("query")
    if query:
        results=events.find_event(query)
    else:
        query=""
        results=[]
    return render_template("find_event.html", query=query, results=results)

@app.route("/event/<int:event_id>")
def show_event(event_id):
    event=events.get_event(event_id)
    if not event:
        abort(404)
    return render_template("show_event.html",event=event)

@app.route("/new_event")
def new_event():
    require_login()
    cur_date=datetime.now() + timedelta(days=1)
    cur_date=cur_date.strftime("%Y-%m-%dT00:00")
    return render_template("new_event.html",cur_date=cur_date)

@app.route("/add_event", methods=["POST"])
def add_event():
    require_login()
    event_name=request.form["event_name"]
    if not event_name or len(event_name)>50:
        abort(403)

    date_time=request.form["date_time"]
    date_time= datetime.strptime(date_time, "%Y-%m-%dT%H:%M")
    cur_date=datetime.now()+timedelta(days=1)
    if not date_time or date_time.date()<=cur_date.date():
        abort(403)

    description=request.form["description"]
    if not description or len(description)>1000:
        abort(403)
    user_id= session["user_id"]

    events.add_event(event_name, date_time, description, user_id)

    return redirect("/")

@app.route("/edit_event/<int:event_id>")
def edit_event(event_id):
    require_login()
    event=events.get_event(event_id)
    if not event:
        abort(404)
    if event["user_id"]!=session["user_id"]:
        abort(403)
    cur_date=datetime.now() + timedelta(days=1)
    cur_date=cur_date.strftime("%Y-%m-%dT00:00")
    return render_template("edit_event.html", event=event, cur_date=cur_date)

@app.route("/update_event", methods=["POST"])
def update_event():
    event_id=request.form["event_id"]
    event=events.get_event(event_id)
    if not event:
        abort(404)
    if event["user_id"]!=session["user_id"]:
        abort(403)

    date_time=request.form["date_time"]
    date_time= datetime.strptime(date_time, "%Y-%m-%dT%H:%M")
    cur_date=datetime.now()+timedelta(days=1)
    if not date_time or date_time.date()<=cur_date.date():
        abort(403)

    description=request.form["description"]
    if not description or len(description)>1000:
        abort(403)

    events.update_event(event_id, date_time, description)

    return redirect("/event/" + str(event_id))

@app.route("/cancel_event/<int:event_id>", methods=["GET","POST"])
def cancel_event(event_id):
    require_login()
    event=events.get_event(event_id)
    if not event:
        abort(404)
    if event["user_id"]!=session["user_id"]:
        abort(403)

    if request.method=="GET":
        return render_template("cancel_event.html", event=event)

    if request.method=="POST":
        if "cancel" in request.form:
            events.cancel_event(event_id)
            return redirect("/")
        else:
            return redirect("/event/"+str(event_id))

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
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
