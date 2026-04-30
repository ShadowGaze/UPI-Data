import sqlite3
import os
from flask import g

DATABASE = os.environ.get('DATABASE_PATH', 'instance/app.db')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# ── Shared helpers ────────────────────────────────────────────────────────────
def fetchall(db, sql, params=()):
    return db.execute(sql, params).fetchall()


def fetchone(db, sql, params=()):
    return db.execute(sql, params).fetchone()


def get_distinct(db, table, col):
    rows = fetchall(
        db, f"SELECT DISTINCT {col} FROM {table} WHERE {col} IS NOT NULL ORDER BY {col}")
    return [r[0] for r in rows]
