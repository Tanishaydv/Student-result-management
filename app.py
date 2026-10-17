from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "students.db"

SUBJECTS = ["English", "Mathematics", "Computer Science", "Physics", "Chemistry"]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_no TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                course TEXT NOT NULL,
                english INTEGER NOT NULL,
                mathematics INTEGER NOT NULL,
                computer_science INTEGER NOT NULL,
                physics INTEGER NOT NULL,
                chemistry INTEGER NOT NULL
            )
        """)

def result_for(student):
    marks = [student[s.lower().replace(" ", "_")] for s in SUBJECTS]
    total = sum(marks)
    percentage = total / len(SUBJECTS)
    passed = all(mark >= 33 for mark in marks)
    if not passed:
        grade = "F"
        status = "Fail"
    elif percentage >= 90:
        grade = "A+"
        status = "Pass"
    elif percentage >= 80:
        grade = "A"
        status = "Pass"
    elif percentage >= 70:
        grade = "B"
        status = "Pass"
    elif percentage >= 60:
        grade = "C"
        status = "Pass"
    elif percentage >= 50:
        grade = "D"
        status = "Pass"
    else:
        grade = "E"
        status = "Pass"
    return {"total": total, "percentage": percentage, "grade": grade, "status": status}

@app.route("/")
def index():
    search = request.args.get("q", "").strip()
    with get_db() as conn:
        if search:
            rows = conn.execute(
                "SELECT * FROM students WHERE name LIKE ? OR roll_no LIKE ? ORDER BY name",
                (f"%{search}%", f"%{search}%")
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM students ORDER BY name").fetchall()
    students = [{"student": row, "result": result_for(row)} for row in rows]
    stats = {
        "total": len(rows),
        "passed": sum(item["result"]["status"] == "Pass" for item in students),
        "failed": sum(item["result"]["status"] == "Fail" for item in students),
    }
    return render_template("index.html", students=students, stats=stats, q=search)

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        data = request.form
        roll_no = data.get("roll_no", "").strip()
        name = data.get("name", "").strip()
        course = data.get("course", "").strip()
        try:
            marks = [int(data.get(field, "")) for field in
                     ["english", "mathematics", "computer_science", "physics", "chemistry"]]
            if not roll_no or not name or not course:
                raise ValueError("Please complete all student details.")
            if any(mark < 0 or mark > 100 for mark in marks):
                raise ValueError("Marks must be between 0 and 100.")
            with get_db() as conn:
                conn.execute("""
                    INSERT INTO students
                    (roll_no, name, course, english, mathematics, computer_science, physics, chemistry)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (roll_no, name, course, *marks))
            flash("Student result added successfully.", "success")
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash("That roll number already exists. Please use a unique roll number.", "error")
        except ValueError as exc:
            flash(str(exc) or "Enter valid marks for every subject.", "error")
    return render_template("student_form.html", student=None, page_title="Add Student")

@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    with get_db() as conn:
        student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if student is None:
        flash("Student not found.", "error")
        return redirect(url_for("index"))
    if request.method == "POST":
        data = request.form
        try:
            marks = [int(data.get(field, "")) for field in
                     ["english", "mathematics", "computer_science", "physics", "chemistry"]]
            roll_no = data.get("roll_no", "").strip()
            name = data.get("name", "").strip()
            course = data.get("course", "").strip()
            if not roll_no or not name or not course:
                raise ValueError("Please complete all student details.")
            if any(mark < 0 or mark > 100 for mark in marks):
                raise ValueError("Marks must be between 0 and 100.")
            with get_db() as conn:
                conn.execute("""
                    UPDATE students SET roll_no=?, name=?, course=?, english=?, mathematics=?,
                    computer_science=?, physics=?, chemistry=? WHERE id=?
                """, (roll_no, name, course, *marks, student_id))
            flash("Student record updated.", "success")
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash("That roll number already exists. Please use a unique roll number.", "error")
        except ValueError as exc:
            flash(str(exc) or "Enter valid marks for every subject.", "error")
        with get_db() as conn:
            student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    return render_template("student_form.html", student=student, page_title="Edit Student")

@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    with get_db() as conn:
        conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    flash("Student record deleted.", "success")
    return redirect(url_for("index"))

@app.route("/result/<int:student_id>")
def view_result(student_id):
    with get_db() as conn:
        student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if student is None:
        flash("Student not found.", "error")
        return redirect(url_for("index"))
    return render_template("result.html", student=student, result=result_for(student), subjects=SUBJECTS)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
