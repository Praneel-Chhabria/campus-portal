"""MySQL access: one connection pool plus small helpers."""
import os
from contextlib import contextmanager

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import pooling

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "school_portal")

_pool = None


def _config(with_database=True):
    cfg = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "charset": "utf8mb4",
    }
    if with_database:
        cfg["database"] = DB_NAME
    return cfg


def server_connection():
    """Connection without a selected database (used by setup_db.py)."""
    return mysql.connector.connect(**_config(with_database=False))


def _get_pool():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name="portal", pool_size=5, **_config()
        )
    return _pool


@contextmanager
def connection():
    conn = _get_pool().get_connection()
    try:
        yield conn
    finally:
        conn.close()  # hands the connection back to the pool


def query(sql, params=None):
    """Run a SELECT and return a list of dicts."""
    with connection() as conn:
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(sql, params or ())
            return cur.fetchall()
        finally:
            cur.close()


def execute(sql, params=None):
    """Run a single INSERT/UPDATE/DELETE and return the affected row count."""
    with connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(sql, params or ())
            conn.commit()
            return cur.rowcount
        finally:
            cur.close()


@contextmanager
def transaction():
    """Yield a cursor; commit on success, roll back on any error."""
    with connection() as conn:
        cur = conn.cursor(dictionary=True)
        try:
            yield cur
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()
