import db

def add_event(event_name, date_time, description, user_id):
    sql = "INSERT INTO events (event_name, date_time, description, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [event_name, date_time, description, user_id])

def get_events():
    sql="SELECT id, date_time, event_name FROM events WHERE date(date_time)>=date('now') ORDER BY date_time DESC"
    return db.query(sql)

def get_event(event_id):
    sql= """SELECT events.date_time, events.event_name, events.description, users.username
            FROM events, users
            WHERE events.user_id = users.id AND events.id = ?"""
    return db.query(sql,[event_id])[0]