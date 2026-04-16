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

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    content TEXT,
    event_id INTEGER REFERENCES events,
    user_id INTEGER REFERENCES users
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE event_classes (
    id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES events,
    title TEXT,
    value TEXT
);