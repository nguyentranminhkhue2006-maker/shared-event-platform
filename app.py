import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session, flash
from datetime import datetime, timedelta
import db
import config
import events, users

app = Flask(__name__)
app.secret_key=config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_events= events.get_events()
    return render_template("index.html", events=all_events)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user=users.get_user(user_id)
    if not user:
        abort(404)
    events=users.get_events(user_id)
    return render_template("show_user.html",user=user, events=events)

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
    classes=events.get_classes(event_id)
    return render_template("show_event.html",event=event, classes=classes)

@app.route("/new_event")
def new_event():
    require_login()
    classes=events.get_all_classes()
    cur_date=datetime.now() + timedelta(days=1)
    cur_date=cur_date.strftime("%Y-%m-%dT00:00")
    return render_template("new_event.html",cur_date=cur_date, classes=classes)

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

    classes=[]
    for entry in request.form.getlist("classes"):
        if entry:
            parts=entry.split(":")
            classes.append((parts[0],parts[1]))

    events.add_event(event_name, date_time, description, user_id, classes)

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

    all_classes=events.get_all_classes()
    classes={}
    for my_classes in all_classes:
        classes[my_classes]=""
    for entry in events.get_classes(event_id):
        classes[entry["title"]]=entry["value"]

    return render_template("edit_event.html", event=event, cur_date=cur_date, all_classes=all_classes, classes=classes)

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

    classes=[]
    for entry in request.form.getlist("classes"):
        if entry:
            parts=entry.split(":")
            classes.append((parts[0],parts[1]))

    events.update_event(event_id, date_time, description, classes)

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

    if not username or len(username)>25 or not password1 or not password2:
        flash('Invalid username or password')
        return render_template("register.html")
    if password1 != password2:
        flash('Passwords must be the same')
        return render_template('register.html')

    try:
        users.create_user(username,password1)
    except sqlite3.IntegrityError:
        flash("Username is already taken")
        return render_template('register.html')

    flash("Account created!")
    return redirect('/')
    

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template('login.html')
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or len(username)>25 or not password:
            abort(403)

        user_id=users.check_login(username,password)
        if user_id:
            session["user_id"]= user_id
            session["username"] = username
            return redirect("/")

        flash('Incorrect username or password')
        return render_template('login.html')


@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
