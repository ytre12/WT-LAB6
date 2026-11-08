import secrets
import sqlite3
from pathlib import Path
from threading import RLock
from time import time

from flask import (
    Flask, abort, g, redirect, render_template, request, url_for,
)

DATABASE = Path(__file__).with_name("points.db")

app = Flask(__name__)

COOKIE_NAME = "session_id"
SESSION_TTL = 30 * 60
sessions = {}
sessions_lock = RLock()

# Лише для локального навчального HTTP; для HTTPS задайте True.
app.config["SESSION_COOKIE_SECURE"] = False


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def create_session(user_id=None):
    sid = secrets.token_urlsafe(32)
    state = {
        "user_id": user_id,
        "csrf_token": secrets.token_urlsafe(32),
        "expires_at": time() + SESSION_TTL,
    }
    with sessions_lock:
        sessions[sid] = state
    return sid, state.copy()


def remove_session(sid):
    with sessions_lock:
        sessions.pop(sid, None)


def set_session_cookie(response, sid):
    response.set_cookie(
        COOKIE_NAME, sid, max_age=SESSION_TTL,
        httponly=True, secure=app.config["SESSION_COOKIE_SECURE"],
        samesite="Lax", path="/",
    )


@app.before_request
def load_current_user():
    g.sid = request.cookies.get(COOKIE_NAME)
    g.auth_session = None
    g.user = None
    now = time()
    with sessions_lock:
        expired = [
            sid for sid, state in sessions.items()
            if state["expires_at"] <= now
        ]
        for sid in expired:
            sessions.pop(sid, None)
        state = sessions.get(g.sid)
        if state is not None:
            g.auth_session = state.copy()
    if g.auth_session and g.auth_session["user_id"] is not None:
        g.user = get_db().execute(
            "SELECT id, username FROM users WHERE id = ?",
            (g.auth_session["user_id"],),
        ).fetchone()
        if g.user is None:
            remove_session(g.sid)
            g.auth_session = None


@app.context_processor
def session_template_data():
    return {
        "csrf_token": (
            g.auth_session["csrf_token"] if g.auth_session else ""
        ),
    }


@app.after_request
def prevent_sensitive_caching(response):
    response.headers["Cache-Control"] = "no-store"
    return response


@app.route("/")
def index():
    db = get_db()
    students = db.execute(
        """
        SELECT * FROM student
        """
    )
    return render_template("main.html", students=students)

@app.route("/courses")
def courses():
    db = get_db()
    courses = db.execute(
        """
        SELECT * FROM course
        """
    )
    return render_template("courses.html", courses=courses)

@app.route("/all_grades")
def all_grades():
    db = get_db()
    all_grades = db.execute(
        """
        SELECT p.id AS grade_id,
               s.name AS name,
               c.title AS course,
               c.semester,
               p.value AS grades
        FROM points AS p
        JOIN student AS s ON s.id = p.id_student
        JOIN course AS c ON c.id = p.id_course
        """
    )
    return render_template("all_grades.html", grades=all_grades,
                           saved=request.args.get("saved") == "1",
                           deleted=request.args.get("deleted") == "1")


@app.route("/grades/<int:grade_id>/edit", methods=["GET", "POST"])
def edit_grade(grade_id):
    db = get_db()

    grade = db.execute(
        """
        SELECT p.id, p.id_student, p.id_course, p.value,
               c.semester
        FROM points AS p
        JOIN course AS c ON c.id = p.id_course
        WHERE p.id = ?
        """,
        (grade_id,),
    ).fetchone()
    if grade is None:
        abort(404)

    students = db.execute(
        "SELECT id, name FROM student ORDER BY name"
    ).fetchall()
    courses = db.execute(
        "SELECT id, title, semester FROM course ORDER BY semester, title"
    ).fetchall()

    error = None
    form = {
        "student_id": str(grade["id_student"]),
        "course_id": str(grade["id_course"]),
        "value": "" if grade["value"] is None else str(grade["value"]),
    }

    if request.method == "POST":
        form["student_id"] = request.form.get("student_id", "")
        form["course_id"] = request.form.get("course_id", "")
        form["value"] = request.form.get("value", "").strip()

        try:
            student_id = int(form["student_id"])
            course_id = int(form["course_id"])
            value = int(form["value"])
        except ValueError:
            error = "Оберіть студента й дисципліну та введіть ціле число."
        else:
            if not 0 <= value <= 100:
                error = "Оцінка має бути від 0 до 100 включно."
            elif db.execute(
                "SELECT 1 FROM student WHERE id = ?", (student_id,)
            ).fetchone() is None:
                error = "Такого студента не існує."
            elif db.execute(
                "SELECT 1 FROM course WHERE id = ?", (course_id,)
            ).fetchone() is None:
                error = "Такої дисципліни не існує."
            else:
                with db:
                    db.execute(
                        """
                        UPDATE points
                        SET id_student = ?, id_course = ?, value = ?
                        WHERE id = ?
                        """,
                        (student_id, course_id, value, grade_id),
                    )
                return redirect(url_for("all_grades", saved=1))

    return render_template(
        "edit_grade.html",
        grade=grade,
        students=students,
        courses=courses,
        form=form,
        error=error,
    )


@app.route("/grades/<int:grade_id>/delete", methods=["POST"])
def delete_grade(grade_id):
    db = get_db()

    grade = db.execute(
        "SELECT id FROM points WHERE id = ?", (grade_id,)
    ).fetchone()
    if grade is None:
        abort(404)

    with db:
        db.execute("DELETE FROM points WHERE id = ?", (grade_id,))

    return redirect(url_for("all_grades", deleted=1))

@app.route("/rating/<int:course_id>/rating")
def rating(course_id):
    db = get_db()

    course = db.execute(
        "SELECT id, title FROM course WHERE id = ?", (course_id,)
    ).fetchone()
    if course is None:
        abort(404)

    rating = db.execute(
        """
        SELECT s.name as name, g.value as grades, c.title as title
        FROM course as c 
        JOIN points as g ON c.id = g.id_course
        JOIN student as s ON s.id = g.id_student
        WHERE c.id = ?
        ORDER BY grades DESC
        """, (course_id,)
    ).fetchall()

    return render_template('rating.html', course=course, rating=rating)

@app.route("/grades/new", methods=["GET", "POST"])
def new_grade():
    db = get_db()

    students = db.execute(
        "SELECT id, name FROM student ORDER BY name"
    ).fetchall()
    courses = db.execute(
        "SELECT id, title, semester FROM course ORDER BY semester, title"
    ).fetchall()

    error = None
    success = None
    form = {"student_id": "", "course_id": "", "value": ""}

    if request.method == "POST":
        form["student_id"] = request.form.get("student_id", "")
        form["course_id"] = request.form.get("course_id", "")
        form["value"] = request.form.get("value", "").strip()

        try:
            student_id = int(form["student_id"])
            course_id = int(form["course_id"])
            value = int(form["value"])
        except ValueError:
            error = "Оберіть студента й дисципліну та введіть ціле число."
        else:
            if not 0 <= value <= 100:
                error = "Оцінка має бути від 0 до 100 включно."
            elif db.execute(
                "SELECT 1 FROM student WHERE id = ?", (student_id,)
            ).fetchone() is None:
                error = "Такого студента не існує."
            elif db.execute(
                "SELECT 1 FROM course WHERE id = ?", (course_id,)
            ).fetchone() is None:
                error = "Такої дисципліни не існує."
            else:
                with db:
                    db.execute(
                        """
                        INSERT INTO points (id_student, id_course, value)
                        VALUES (?, ?, ?)
                        """,
                        (student_id, course_id, value),
                    )
                success = f"Оцінку {value} додано."
                form = {"student_id": "", "course_id": "", "value": ""}

    return render_template(
        "new_grades.html",
        students=students,
        courses=courses,
        error=error,
        success=success,
        form=form,
    )


@app.route("/student/<int:student_id>/grades")
def student_grades(student_id):
    db = get_db()

    student = db.execute(
        "SELECT id, name FROM student WHERE id = ?", (student_id,)
    ).fetchone()
    if student is None:
        abort(404)

    grades = db.execute(
        """
        SELECT c.title, c.semester, p.value
        FROM points AS p
        JOIN course AS c ON c.id = p.id_course
        WHERE p.id_student = ?
        """,
        (student_id,),
    ).fetchall()

    return render_template("grades.html", student=student, grades=grades)

@app.route("/courses/avg")
def avg():
    db = get_db()

    avg = db.execute(
        """
        SELECT c.id, c.title, ROUND(AVG(g.value), 2) AS avg_grade
        FROM course AS c
        LEFT JOIN points AS g ON g.id_course = c.id
        GROUP BY c.id, c.title
        """
    ).fetchall()

    return render_template("avg.html", avg=avg)

@app.route("/course/ects")
def course_ects():
    db = get_db()

    rows = db.execute(
        """
        WITH classified AS (
            SELECT p.id_course AS subject_id,
                   CASE
                       WHEN p.value IS NULL OR p.value < 0 OR p.value > 100 THEN 'INVALID'
                       WHEN p.value >= 90 THEN 'A'
                       WHEN p.value >= 82 THEN 'B'
                       WHEN p.value >= 75 THEN 'C'
                       WHEN p.value >= 64 THEN 'D'
                       WHEN p.value >= 60 THEN 'E'
                       WHEN p.value >= 35 THEN 'FX'
                       ELSE 'F'
                   END AS ects
            FROM points AS p
        )
        SELECT c.id AS subject_id,
               c.title AS subject_name,
               cl.ects,
               COUNT(cl.ects) AS grade_count
        FROM course AS c
        LEFT JOIN classified AS cl ON cl.subject_id = c.id
        GROUP BY c.id, c.title, cl.ects
        ORDER BY c.title, c.id
        """
    ).fetchall()

    letters = ["A", "B", "C", "D", "E", "FX", "F", "INVALID"]

    table = {}
    for r in rows:
        course = table.setdefault(
            r["subject_id"],
            {
                "title": r["subject_name"],
                "counts": {letter: 0 for letter in letters},
                "total": 0,
            },
        )
        if r["ects"] is not None:
            course["counts"][r["ects"]] = r["grade_count"]
            course["total"] += r["grade_count"]

    table = sorted(table.values(), key=lambda row: row["title"])

    return render_template("ects_course.html", table=table, letters=letters)


@app.route("/students/ects")
def students_ects():
    db = get_db()

    rows = db.execute(
        """
        WITH classified AS (
            SELECT p.id_student AS student_id,
                   c.semester,
                   CASE
                       WHEN p.value IS NULL OR p.value < 0 OR p.value > 100 THEN 'INVALID'
                       WHEN p.value >= 90 THEN 'A'
                       WHEN p.value >= 82 THEN 'B'
                       WHEN p.value >= 75 THEN 'C'
                       WHEN p.value >= 64 THEN 'D'
                       WHEN p.value >= 60 THEN 'E'
                       WHEN p.value >= 35 THEN 'FX'
                       ELSE 'F'
                   END AS ects
            FROM points AS p
            JOIN course AS c ON c.id = p.id_course
        )
        SELECT s.id, s.name AS full_name, cl.semester, cl.ects,
               COUNT(*) AS grade_count
        FROM classified AS cl
        JOIN student AS s ON s.id = cl.student_id
        GROUP BY s.id, s.name, cl.semester, cl.ects
        ORDER BY s.name, s.id, cl.semester,
                 CASE cl.ects
                     WHEN 'A' THEN 1 WHEN 'B' THEN 2 WHEN 'C' THEN 3
                     WHEN 'D' THEN 4 WHEN 'E' THEN 5 WHEN 'FX' THEN 6
                     WHEN 'F' THEN 7 ELSE 8
                 END
        """
    ).fetchall()

    return render_template("students_ects.html", rows=rows)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
