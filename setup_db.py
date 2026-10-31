"""One time setup.

    python setup_db.py            creates the database, tables, all MIT-WPU programmes and the first admin
    python setup_db.py --sample   also adds sample teachers, subjects and students to try the portal
"""
import argparse
import getpass
import sys
from pathlib import Path

import auth
import catalog
import db
import services

SAMPLE_PROGRAM = "B.Tech Computer Science and Engineering (Artificial Intelligence and Data Science)"
SAMPLE_SEMESTER = 3
SAMPLE_SUBJECTS = [
    ("Data Structures and Algorithms (Linear)", 4),
    ("Database Management Systems", 4),
    ("Operating Systems", 3),
    ("Linear Algebra for Data Science", 3),
    ("C Programming", 3),
]
SAMPLE_TEACHERS = [("Demo Teacher One", "demo.teacher1"), ("Demo Teacher Two", "demo.teacher2")]
# (PRN, name, attendance, marks in the order of SAMPLE_SUBJECTS). None means not entered yet.
SAMPLE_STUDENTS = [
    ("1262251874", "Praneel Chhabria", None, [None] * 5),
    ("1262250001", "Sample Student One", 92, [88, 91, 79, 84, 95]),
    ("1262250002", "Sample Student Two", 68, [54, 47, 62, 39, 71]),
]


def create_schema():
    conn = db.server_connection()
    cur = conn.cursor()
    cur.execute(
        f"CREATE DATABASE IF NOT EXISTS `{db.DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci"
    )
    cur.execute(f"USE `{db.DB_NAME}`")
    cur.execute("SHOW TABLES LIKE 'classes'")
    if cur.fetchone():
        sys.exit(
            f"The database '{db.DB_NAME}' holds the old school version of this portal.\n"
            "Set DB_NAME in .env to a new name (for example mitwpu_portal) and run this again."
        )
    script = (Path(__file__).parent / "schema.sql").read_text(encoding="utf-8")
    for statement in script.split(";"):
        if statement.strip():
            cur.execute(statement)
    conn.commit()
    cur.close()
    conn.close()
    print(f"Database '{db.DB_NAME}' and tables are ready.")


def seed_programmes():
    for name in catalog.SCHOOLS:
        db.execute("INSERT IGNORE INTO schools (name) VALUES (%s)", (name,))
    school_ids = {r["name"]: r["id"] for r in db.query("SELECT id, name FROM schools")}
    for school, level, name, years in catalog.PROGRAMMES:
        db.execute(
            "INSERT IGNORE INTO programs (school_id, level, name, semesters) VALUES (%s, %s, %s, %s)",
            (school_ids[school], level, name, catalog.semesters(years)),
        )
    total = db.query("SELECT COUNT(*) AS n FROM programs")[0]["n"]
    print(f"{total} MIT-WPU programmes loaded.")


def create_first_admin():
    if db.query("SELECT 1 FROM users WHERE role = 'admin' LIMIT 1"):
        print("An admin account already exists, skipping.")
        return
    print("\nCreate the first admin account.")
    username = input("Admin username [admin]: ").strip() or "admin"
    while True:
        password = getpass.getpass("Admin password (8+ characters, letters and numbers): ")
        problem = auth.password_problem(password)
        if problem:
            print(problem)
            continue
        if password != getpass.getpass("Repeat password: "):
            print("Passwords do not match.")
            continue
        try:
            services.create_admin(username, password)
        except ValueError as error:
            print(error)
            username = input("Admin username: ").strip()
            continue
        break
    print(f"Admin '{username}' created.")


def seed_sample_data():
    program_id = db.query("SELECT id FROM programs WHERE name = %s", (SAMPLE_PROGRAM,))[0]["id"]
    credentials = []

    subject_ids = []
    for name, credits in SAMPLE_SUBJECTS:
        try:
            services.add_subject(program_id, SAMPLE_SEMESTER, name, credits)
        except ValueError:
            pass
        subject_ids.append(
            db.query(
                "SELECT id FROM subjects WHERE program_id = %s AND semester = %s AND name = %s",
                (program_id, SAMPLE_SEMESTER, name),
            )[0]["id"]
        )

    for index, (full_name, username) in enumerate(SAMPLE_TEACHERS):
        try:
            result = services.create_teacher(username, full_name)
        except ValueError as error:
            print(f"Skipped teacher {full_name}: {error}")
            continue
        credentials.append(("teacher", full_name, result["username"], result["password"]))
        for position, subject_id in enumerate(subject_ids):
            if position % len(SAMPLE_TEACHERS) == index:
                services.assign_teacher(result["teacher_id"], subject_id)

    for prn, name, attendance, marks in SAMPLE_STUDENTS:
        try:
            result = services.create_student(prn, name, program_id, SAMPLE_SEMESTER)
        except ValueError as error:
            print(f"Skipped student {name}: {error}")
            continue
        credentials.append(("student", name, result["username"], result["password"]))
        for subject_id, mark in zip(subject_ids, marks):
            if mark is not None or attendance is not None:
                db.execute(
                    "UPDATE subject_records SET marks = %s, attendance = %s WHERE student_id = %s AND subject_id = %s",
                    (mark, attendance, result["student_id"], subject_id),
                )

    if credentials:
        print("\nSample accounts (temporary passwords, shown once, everyone must change theirs at first sign in):")
        print(f"{'role':<9}{'name':<22}{'username':<18}password")
        for role, name, username, password in credentials:
            print(f"{role:<9}{name:<22}{username:<18}{password}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", action="store_true", help="add sample teachers, subjects and students")
    args = parser.parse_args()

    create_schema()
    seed_programmes()
    create_first_admin()
    if args.sample:
        seed_sample_data()
    print("\nDone. Start the app with: streamlit run app.py")
