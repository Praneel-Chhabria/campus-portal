"""Admin operations: students, teachers, programmes, subjects, promotion."""
import re

from mysql.connector import errors

import auth
import db

USERNAME_RE = re.compile(r"^[a-z0-9._]{3,30}$")
PRN_RE = re.compile(r"^[A-Za-z0-9]{5,20}$")


def sync_records():
    """Make sure every student has an empty record for each subject of their current semester."""
    db.execute(
        "INSERT IGNORE INTO subject_records (student_id, subject_id) "
        "SELECT st.id, sub.id FROM students st "
        "JOIN subjects sub ON sub.program_id = st.program_id AND sub.semester = st.semester"
    )


def _program(program_id):
    rows = db.query("SELECT id, name, semesters FROM programs WHERE id = %s", (program_id,))
    if not rows:
        raise ValueError("Choose a programme.")
    return rows[0]


def create_student(prn, full_name, program_id, semester):
    prn = prn.strip()
    full_name = full_name.strip()
    if not PRN_RE.match(prn):
        raise ValueError("PRN must be 5 to 20 letters or digits.")
    if not full_name:
        raise ValueError("Enter the student's name.")
    program = _program(program_id)
    if not 1 <= int(semester) <= program["semesters"]:
        raise ValueError(f"This programme has {program['semesters']} semesters.")

    username = prn.lower()
    password = auth.generate_temp_password()
    password_hash = auth.hash_password(password)
    try:
        with db.transaction() as cur:
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, 'student')",
                (username, password_hash),
            )
            cur.execute(
                "INSERT INTO students (user_id, prn, full_name, program_id, semester) VALUES (%s, %s, %s, %s, %s)",
                (cur.lastrowid, prn, full_name, program_id, int(semester)),
            )
            student_id = cur.lastrowid
    except errors.IntegrityError:
        raise ValueError(f"A student with PRN {prn} already exists.")
    sync_records()
    return {"student_id": student_id, "username": username, "password": password}


def create_teacher(username, full_name):
    username = username.strip().lower()
    full_name = full_name.strip()
    if not full_name:
        raise ValueError("Enter the teacher's name.")
    if not USERNAME_RE.match(username):
        raise ValueError("Username must be 3 to 30 characters: lowercase letters, numbers, dots or underscores.")

    password = auth.generate_temp_password()
    password_hash = auth.hash_password(password)
    try:
        with db.transaction() as cur:
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, 'teacher')",
                (username, password_hash),
            )
            cur.execute("INSERT INTO teachers (user_id, full_name) VALUES (%s, %s)", (cur.lastrowid, full_name))
            teacher_id = cur.lastrowid
    except errors.IntegrityError:
        raise ValueError(f"The username {username} is already taken.")
    return {"teacher_id": teacher_id, "username": username, "password": password}


def create_admin(username, password):
    username = username.strip().lower()
    if not USERNAME_RE.match(username):
        raise ValueError("Username must be 3 to 30 characters: lowercase letters, numbers, dots or underscores.")
    problem = auth.password_problem(password)
    if problem:
        raise ValueError(problem)
    try:
        db.execute(
            "INSERT INTO users (username, password_hash, role, must_change_password) "
            "VALUES (%s, %s, 'admin', FALSE)",
            (username, auth.hash_password(password)),
        )
    except errors.IntegrityError:
        raise ValueError(f"The username {username} is already taken.")


def delete_user(user_id, acting_user_id):
    """Remove a student or teacher. Their profile, marks, attendance and assignments go with them."""
    if user_id == acting_user_id:
        raise ValueError("You cannot remove your own account.")
    removed = db.execute("DELETE FROM users WHERE id = %s AND role IN ('student', 'teacher')", (user_id,))
    if not removed:
        raise ValueError("That account no longer exists.")


def reset_password(user_id):
    """Set a new temporary password, force a change at next sign in, and unlock the account."""
    password = auth.generate_temp_password()
    db.execute(
        "UPDATE users SET password_hash = %s, must_change_password = TRUE, "
        "failed_attempts = 0, locked_until = NULL WHERE id = %s",
        (auth.hash_password(password), user_id),
    )
    return password


def promote(program_id, semester):
    """Move every student of a programme from one semester to the next. Returns how many moved."""
    program = _program(program_id)
    semester = int(semester)
    if semester >= program["semesters"]:
        raise ValueError(f"Semester {semester} is the last semester of this programme.")
    moved = db.execute(
        "UPDATE students SET semester = semester + 1 WHERE program_id = %s AND semester = %s",
        (program_id, semester),
    )
    sync_records()
    return moved


def add_subject(program_id, semester, name, credits, code=None):
    name = name.strip()
    code = (code or "").strip() or None
    program = _program(program_id)
    if not name:
        raise ValueError("Enter the subject name.")
    if not 1 <= int(semester) <= program["semesters"]:
        raise ValueError(f"This programme has {program['semesters']} semesters.")
    try:
        db.execute(
            "INSERT INTO subjects (program_id, semester, code, name, credits) VALUES (%s, %s, %s, %s, %s)",
            (program_id, int(semester), code, name, int(credits)),
        )
    except errors.IntegrityError:
        raise ValueError(f"{name} is already a subject in semester {semester}.")
    sync_records()


def delete_subject(subject_id):
    removed = db.execute("DELETE FROM subjects WHERE id = %s", (subject_id,))
    if not removed:
        raise ValueError("That subject no longer exists.")


def assign_teacher(teacher_id, subject_id):
    db.execute("INSERT IGNORE INTO teaching (teacher_id, subject_id) VALUES (%s, %s)", (teacher_id, subject_id))


def unassign_teacher(teacher_id, subject_id):
    db.execute("DELETE FROM teaching WHERE teacher_id = %s AND subject_id = %s", (teacher_id, subject_id))


def add_program(school_id, level, name, semesters):
    name = name.strip()
    if not name:
        raise ValueError("Enter the programme name.")
    try:
        db.execute(
            "INSERT INTO programs (school_id, level, name, semesters) VALUES (%s, %s, %s, %s)",
            (school_id, level, name, int(semesters)),
        )
    except errors.IntegrityError:
        raise ValueError("A programme with that name already exists.")


def set_semesters(program_id, semesters):
    semesters = int(semesters)
    used = db.query(
        "SELECT GREATEST(COALESCE((SELECT MAX(semester) FROM students WHERE program_id = %s), 1), "
        "COALESCE((SELECT MAX(semester) FROM subjects WHERE program_id = %s), 1)) AS top",
        (program_id, program_id),
    )[0]["top"]
    if semesters < used:
        raise ValueError(f"Students or subjects already use semester {used}. Pick {used} or more.")
    db.execute("UPDATE programs SET semesters = %s WHERE id = %s", (semesters, program_id))
