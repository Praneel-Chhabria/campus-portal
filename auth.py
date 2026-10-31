"""Passwords, login checks and lockout."""
import re
import secrets

import bcrypt

import db

MAX_ATTEMPTS = 5
LOCK_MINUTES = 15
MIN_LENGTH = 8

_TEMP_ALPHABET = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
# Used so a wrong username takes as long to reject as a wrong password.
_DUMMY_HASH = bcrypt.hashpw(b"not-a-real-password", bcrypt.gensalt(rounds=12))


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("ascii")


def verify_password(password, hashed):
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("ascii"))
    except ValueError:
        return False


def password_problem(password):
    """Return a message describing what is wrong, or None if the password is fine."""
    if len(password) < MIN_LENGTH:
        return f"Use at least {MIN_LENGTH} characters."
    if len(password.encode("utf-8")) > 72:
        return "Use 72 bytes or fewer."
    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        return "Include at least one letter and one number."
    return None


def generate_temp_password():
    return "".join(secrets.choice(_TEMP_ALPHABET) for _ in range(10))


def authenticate(username, password, allowed_roles):
    """Return (user_row, None) on success or (None, error_message)."""
    username = username.strip().lower()
    rows = db.query(
        "SELECT *, (locked_until IS NOT NULL AND locked_until > NOW()) AS is_locked "
        "FROM users WHERE username = %s",
        (username,),
    )
    if not rows:
        bcrypt.checkpw(b"not-a-real-password", _DUMMY_HASH)
        return None, "Username or password is incorrect."

    user = rows[0]
    if user["is_locked"]:
        return None, f"Too many failed attempts. Try again in {LOCK_MINUTES} minutes."

    if not verify_password(password, user["password_hash"]):
        attempts = user["failed_attempts"] + 1
        if attempts >= MAX_ATTEMPTS:
            db.execute(
                "UPDATE users SET failed_attempts = 0, "
                "locked_until = NOW() + INTERVAL %s MINUTE WHERE id = %s",
                (LOCK_MINUTES, user["id"]),
            )
        else:
            db.execute(
                "UPDATE users SET failed_attempts = %s WHERE id = %s",
                (attempts, user["id"]),
            )
        return None, "Username or password is incorrect."

    if user["role"] not in allowed_roles:
        return None, "This account signs in on the other tab."

    db.execute(
        "UPDATE users SET failed_attempts = 0, locked_until = NULL, "
        "last_login = NOW() WHERE id = %s",
        (user["id"],),
    )
    return user, None


def build_session(user):
    """Turn a users row into the small dict kept in st.session_state."""
    session = {
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "must_change": bool(user["must_change_password"]),
        "name": "Administrator" if user["role"] == "admin" else user["username"],
    }
    if user["role"] == "teacher":
        rows = db.query("SELECT id, full_name FROM teachers WHERE user_id = %s", (user["id"],))
        if rows:
            session.update(name=rows[0]["full_name"], teacher_id=rows[0]["id"])
    elif user["role"] == "student":
        rows = db.query(
            "SELECT st.id, st.prn, st.full_name, st.semester, p.name AS program, p.semesters "
            "FROM students st JOIN programs p ON p.id = st.program_id WHERE st.user_id = %s",
            (user["id"],),
        )
        if rows:
            session.update(
                name=rows[0]["full_name"], student_id=rows[0]["id"], prn=rows[0]["prn"],
                program=rows[0]["program"], semester=rows[0]["semester"],
            )
    return session


def check_current_password(user_id, password):
    rows = db.query("SELECT password_hash FROM users WHERE id = %s", (user_id,))
    return bool(rows) and verify_password(password, rows[0]["password_hash"])


def change_password(user_id, new_password):
    db.execute(
        "UPDATE users SET password_hash = %s, must_change_password = FALSE WHERE id = %s",
        (hash_password(new_password), user_id),
    )
