import sqlite3
from datetime import date, timedelta
import random

DB_PATH = "spendly.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            email         TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at    TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL NOT NULL,
            category    TEXT NOT NULL,
            date        TEXT NOT NULL,
            description TEXT,
            created_at  TEXT DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


def email_exists(email):
    conn = get_db()
    row = conn.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return row is not None


def create_user(name, email, password_hash):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash),
    )
    user_id = cur.lastrowid
    conn.commit()
    conn.close()
    return user_id


def seed_db():
    from werkzeug.security import generate_password_hash

    conn = get_db()

    if conn.execute("SELECT 1 FROM users LIMIT 1").fetchone():
        conn.close()
        return

    cur = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    demo_id = cur.lastrowid

    today = date.today()
    sample_expenses = [
        ("Food",          120.0,  "Lunch at canteen"),
        ("Transport",     45.0,   "Auto rickshaw to office"),
        ("Bills",         850.0,  "Electricity bill"),
        ("Health",        300.0,  "Pharmacy — vitamins"),
        ("Entertainment", 250.0,  "Movie ticket"),
        ("Shopping",      1200.0, "New shirt from Myntra"),
        ("Other",         75.0,   "Stationery"),
        ("Food",          90.0,   "Dinner — Zomato order"),
    ]

    for i, (category, amount, description) in enumerate(sample_expenses):
        expense_date = (today - timedelta(days=i * 3)).strftime("%Y-%m-%d")
        conn.execute(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            (demo_id, amount, category, expense_date, description),
        )

    conn.commit()
    conn.close()
