import sqlite3
from datetime import date, datetime
from pathlib import Path

from database.migrations import run_migrations, seed_default_modules


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "rise.db"


def now_iso():
    return datetime.now().isoformat(timespec="seconds")


def today_iso():
    return date.today().isoformat()


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")

    return connection


def initialize_database():
    connection = get_connection()

    try:
        run_migrations(connection)
        seed_default_modules(connection)
        connection.commit()
    finally:
        connection.close()


def has_user_profile():
    connection = get_connection()

    try:
        row = connection.execute("SELECT id FROM users LIMIT 1;").fetchone()
        return row is not None
    finally:
        connection.close()


def get_first_user():
    connection = get_connection()

    try:
        return connection.execute("SELECT * FROM users LIMIT 1;").fetchone()
    finally:
        connection.close()


def create_initial_profile(name, age, height_cm, current_weight, goal_weight):
    connection = get_connection()
    timestamp = now_iso()
    today = today_iso()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users
            (name, age, height_cm, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?);
            """,
            (name, age, height_cm, timestamp, timestamp),
        )

        user_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO user_settings
            (user_id, theme, offline_mode_enabled, ai_enabled, backup_enabled, created_at, updated_at)
            VALUES (?, 'dark', 1, 0, 1, ?, ?);
            """,
            (user_id, timestamp, timestamp),
        )

        cursor.execute(
            """
            INSERT INTO goals
            (user_id, module_key, title, description, goal_type,
             start_value, current_value, target_value, unit,
             start_date, status, created_at, updated_at)
            VALUES (?, 'health', ?, ?, 'weight',
                    ?, ?, ?, 'kg',
                    ?, 'active', ?, ?);
            """,
            (
                user_id,
                f"Reach {goal_weight} kg",
                "Initial body weight goal created during onboarding.",
                current_weight,
                current_weight,
                goal_weight,
                today,
                timestamp,
                timestamp,
            ),
        )

        cursor.execute(
            """
            INSERT INTO health_weight_logs
            (user_id, date, weight_kg, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?);
            """,
            (user_id, today, current_weight, timestamp, timestamp),
        )

        connection.commit()
        return user_id

    finally:
        connection.close()