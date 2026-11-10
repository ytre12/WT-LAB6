-- Структура бази даних застосунку LAB6.
-- Виконується під час першого запуску, якщо бази ще немає.

CREATE TABLE IF NOT EXISTS student (
    id INTEGER NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (id AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS course (
    id INTEGER NOT NULL,
    title TEXT NOT NULL,
    semester INTEGER NOT NULL,
    PRIMARY KEY (id AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS points (
    id INTEGER NOT NULL,
    id_course INTEGER NOT NULL,
    id_student INTEGER NOT NULL,
    value INTEGER,
    PRIMARY KEY (id AUTOINCREMENT),
    FOREIGN KEY (id_course) REFERENCES course (id),
    FOREIGN KEY (id_student) REFERENCES student (id)
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS app_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
