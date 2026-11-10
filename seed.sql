-- Початкові навчальні дані для points.db / app.sqlite3

-- student
INSERT OR IGNORE INTO student (id, name) VALUES (1, 'Гончаренко Максим Олегович');
INSERT OR IGNORE INTO student (id, name) VALUES (2, 'Савченко Ольга Василівна');
INSERT OR IGNORE INTO student (id, name) VALUES (3, 'Коваль Андрій Петрович');
INSERT OR IGNORE INTO student (id, name) VALUES (4, 'Шевчук Наталія Ігорівна');
INSERT OR IGNORE INTO student (id, name) VALUES (5, 'Мартинюк Сергій Михайлович');

-- course
INSERT OR IGNORE INTO course (id, title, semester) VALUES (1, 'Вступ до комп’ютерних наук', 1);
INSERT OR IGNORE INTO course (id, title, semester) VALUES (2, 'Лінійна алгебра', 1);
INSERT OR IGNORE INTO course (id, title, semester) VALUES (3, 'Алгоритми та структури даних', 2);
INSERT OR IGNORE INTO course (id, title, semester) VALUES (4, 'Системне програмування', 2);
INSERT OR IGNORE INTO course (id, title, semester) VALUES (5, 'Бази даних', 3);
INSERT OR IGNORE INTO course (id, title, semester) VALUES (6, 'Операційні системи', 3);
INSERT OR IGNORE INTO course (id, title, semester) VALUES (7, 'Комп’ютерні мережі', 4);
INSERT OR IGNORE INTO course (id, title, semester) VALUES (8, 'Проектування програмного забезпечення', 4);
INSERT OR IGNORE INTO course (id, title, semester) VALUES (9, 'Мова програмування Python', 5);
INSERT OR IGNORE INTO course (id, title, semester) VALUES (10, 'Теорія ймовірностей та математична статистика', 5);
INSERT OR IGNORE INTO course (id, title, semester) VALUES (11, 'Інформаційна безпека', 6);
INSERT OR IGNORE INTO course (id, title, semester) VALUES (12, 'Вебтехнології', 6);
INSERT OR IGNORE INTO course (id, title, semester) VALUES (13, 'Хмарні обчислення', 7);
INSERT OR IGNORE INTO course (id, title, semester) VALUES (14, 'Мобільна розробка', 7);
INSERT OR IGNORE INTO course (id, title, semester) VALUES (15, 'Управління IT-проєктами', 8);

-- points
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (2, 1, 1, 85);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (3, 1, 2, 92);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (4, 1, 3, 78);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (5, 2, 4, 88);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (6, 2, 5, 74);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (7, 12, 1, 10);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (8, 3, 3, 67);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (9, 3, 5, 82);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (10, 4, 2, 95);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (11, 4, 4, 89);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (12, 5, 1, 93);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (13, 5, 4, 76);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (14, 6, 3, 88);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (15, 6, 5, 81);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (16, 7, 2, 79);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (17, 7, 3, 84);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (18, 8, 4, 90);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (20, 9, 1, 87);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (21, 9, 2, 94);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (22, 10, 3, 69);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (23, 10, 4, 83);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (24, 11, 5, 97);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (25, 12, 1, 88);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (26, 12, 2, 91);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (27, 13, 3, 77);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (28, 13, 4, 85);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (29, 14, 5, 80);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (30, 15, 1, 93);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (31, 15, 2, 75);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (32, 7, 2, 99);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (33, 5, 5, 0);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (34, 12, 4, 90);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (35, 4, 2, 2);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (36, 2, 5, 23);
INSERT OR IGNORE INTO points (id, id_course, id_student, value) VALUES (37, 5, 5, 90);

-- users
INSERT OR IGNORE INTO users (id, username, password_hash) VALUES (1, 'admin', 'pbkdf2:sha256:1000000$XtIlHzj7vHhzmCzi$0c834f18e8d143fc3b49e19f863bbd47a032ea7b3060bdcb1100d3ca6e44517e');
INSERT OR IGNORE INTO users (id, username, password_hash) VALUES (2, 'student', 'pbkdf2:sha256:1000000$FfeoY3Lcrpnk2zPe$608abef0f2865f0ece461937a9ca6389bf99c5e296b2131a34d8b230ee15e461');
INSERT OR IGNORE INTO users (id, username, password_hash) VALUES (3, 'teacher', 'pbkdf2:sha256:1000000$fZHEOnPgqeesc594$ff9fc85014b686f752e731be373afbd335e003996db9537db6313ec35c772262');

