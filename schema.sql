CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    coursename TEXT UNIQUE,
    num_holes NUMBER
);

CREATE TABLE rounds (
    id INTEGER PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    creator_id INTEGER REFERENCES users,
    start_time DATE,
    num_players NUMBER,
    attendees TEXT
);
