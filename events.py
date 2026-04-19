import db
from datetime import datetime

def get_all_classes():
    sql="SELECT title, value FROM classes ORDER BY id"
    result=db.query(sql)

    classes={}
    for title, value in result:
        if title not in classes:
            classes[title]=[]
        classes[title].append(value)

    return classes

def add_event(event_name, date_time, description, user_id, classes):
    date_time=date_time.strftime("%Y-%m-%d %H:%M:%S")
    sql = "INSERT INTO events (event_name, date_time, description, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [event_name, date_time, description, user_id])

    event_id= db.last_insert_id()

    sql="INSERT INTO event_classes (event_id, title, value) VALUES (?,?,?)"
    for title, value in classes:
        db.execute(sql, [event_id,title, value])

def add_comment(event_id, user_id, content):
    sql="INSERT INTO comments (event_id, user_id, content) VALUES (?,?,?)"
    db.execute(sql, [event_id, user_id, content])

def get_comments(event_id):
    sql=""" SELECT comments.content, users.id user_id, users.username FROM comments, users 
            WHERE comments.event_id=? AND comments.user_id=users.id
            ORDER BY comments.id DESC"""
    return db.query(sql, [event_id])

def get_classes(event_id):
    sql="SELECT title, value FROM event_classes WHERE event_id=?"
    return db.query(sql,[event_id])

def get_events():
    sql=""" SELECT events.id, events.date_time, events.event_name, users.id user_id, users.username
            FROM events, users
            WHERE events.user_id=users.id
            ORDER BY events.date_time"""
    return db.query(sql)

def get_event(event_id):
    sql= """SELECT events.id, events.date_time, events.event_name, events.description, users.username, users.id user_id
            FROM events, users
            WHERE events.user_id = users.id AND events.id = ?"""
    result= db.query(sql,[event_id])
    return result[0] if result else None

def update_event(event_id, date_time, description, classes):
    date_time=date_time.strftime("%Y-%m-%d %H:%M:%S")
    sql="""UPDATE events SET date_time = ?, description = ?
                         WHERE id = ?"""
    db.execute(sql, [date_time, description, event_id])

    sql="DELETE FROM event_classes WHERE event_id=?"
    db.execute(sql,[event_id])

    sql="INSERT INTO event_classes (event_id, title, value) VALUES (?,?,?)"
    for title, value in classes:
        db.execute(sql, [event_id,title, value])

def cancel_event(event_id):
    sql="DELETE FROM event_classes WHERE event_id=?"
    db.execute(sql, [event_id])
    sql="DELETE FROM comments WHERE event_id=?"
    db.execute(sql, [event_id])
    sql="DELETE FROM events WHERE id=?"
    db.execute(sql, [event_id])

def find_event(query, classes):
    if classes:
        filter_query=""
        filters=[]
        for title in classes:
            filter_query+="event_classes.title=? AND event_classes.value=? "
            filters.append(title)
            filters.append(classes[title])
    if query and classes:
        like="%"+query+"%"
        sql=""" SELECT DISTINCT events.id, event_name 
                FROM events JOIN event_classes ON events.id=event_classes.event_id
                WHERE (event_name LIKE ? OR description LIKE ?) AND """ 
        sql+= filter_query + "ORDER BY events.id DESC"
        return db.query(sql,[like, like]+filters)
    elif query:
        like="%"+query+"%"
        sql="""SELECT id, event_name FROM events WHERE event_name LIKE ? OR description LIKE ? ORDER BY id DESC"""
        return db.query(sql,[like, like])
    else:
        sql="SELECT DISTINCT events.id, events.event_name FROM events JOIN event_classes ON events.id=event_classes.event_id WHERE "
        sql+= filter_query + "ORDER BY events.id DESC"
        print(sql)
        return db.query(sql,filters)
