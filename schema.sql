CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    coursename TEXT UNIQUE,
    num_holes NUMBER,
    holes TEXT
);

CREATE TABLE rounds (
    id INTEGER PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    course_data TEXT,
    start_time DATE,
    num_players NUMBER
);

CREATE TABLE participations (
    id INTEGER PRIMARY KEY,
    round_id INTEGER REFERENCES rounds,
    participator_id INTEGER REFERENCES users
);
