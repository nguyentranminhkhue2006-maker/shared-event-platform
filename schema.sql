CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    event_name TEXT,
    date_time TIMESTAMP,
    description TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE event_classes (
    id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES events,
    title TEXT
);