import db
from datetime import datetime

def add_event(event_name, date_time, description, user_id):
    date_time= datetime.strptime(date_time, "%Y-%m-%dT%H:%M")
    date_time=date_time.strftime("%Y-%m-%d %H:%M:%S")
    sql = "INSERT INTO events (event_name, date_time, description, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [event_name, date_time, description, user_id])

def get_events():
    sql="SELECT id, date_time, event_name FROM events WHERE date(date_time)>=date('now') ORDER BY date_time"
    return db.query(sql)

def get_event(event_id):
    sql= """SELECT events.id, events.date_time, events.event_name, events.description, users.username, users.id user_id
            FROM events, users
            WHERE events.user_id = users.id AND events.id = ?"""
    return db.query(sql,[event_id])[0]

def update_event(event_id, date_time, description):
    date_time= datetime.strptime(date_time, "%Y-%m-%dT%H:%M")
    date_time=date_time.strftime("%Y-%m-%d %H:%M:%S")
    sql="""UPDATE events SET date_time = ?, description = ?
                         WHERE id = ?"""
    db.execute(sql, [date_time, description, event_id])