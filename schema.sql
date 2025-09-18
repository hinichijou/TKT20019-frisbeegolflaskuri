CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    coursename TEXT UNIQUE,
    num_holes NUMBER,
    hole_data TEXT
);

CREATE TABLE rounds (
    id INTEGER PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    start_time DATE,
    num_players NUMBER,
    coursename TEXT,
    num_holes NUMBER,
    hole_data TEXT
);

CREATE TABLE participations (
    id INTEGER PRIMARY KEY,
    round_id INTEGER REFERENCES rounds,
    participator_id INTEGER REFERENCES users
);

CREATE TABLE selection_classes (
    id INTEGER PRIMARY KEY,
    class_key TEXT UNIQUE
);

CREATE TABLE selection_class_items (
    id INTEGER PRIMARY KEY,
    class_id INTEGER REFERENCES selection_classes,
    item_key TEXT UNIQUE
);

CREATE TABLE course_selections (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES selection_class_items,
    course_id INTEGER REFERENCES courses
);