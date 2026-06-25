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


def calculate_progress(start_value, current_value, target_value):
    if start_value is None or current_value is None or target_value is None:
        return 0

    if start_value == target_value:
        return 100

    # Weight loss goal: 72 -> 65
    if target_value < start_value:
        progress = ((start_value - current_value) / (start_value - target_value)) * 100
    # Weight gain goal: 55 -> 65
    else:
        progress = ((current_value - start_value) / (target_value - start_value)) * 100

    return max(0, min(100, round(progress, 1)))


def get_dashboard_data():
    connection = get_connection()

    try:
        user = connection.execute(
            """
            SELECT *
            FROM users
            ORDER BY id ASC
            LIMIT 1;
            """
        ).fetchone()

        if user is None:
            return None

        weight_goal = connection.execute(
            """
            SELECT *
            FROM goals
            WHERE user_id = ?
              AND module_key = 'health'
              AND goal_type = 'weight'
              AND status = 'active'
            ORDER BY id DESC
            LIMIT 1;
            """,
            (user["id"],),
        ).fetchone()

        latest_weight = connection.execute(
            """
            SELECT *
            FROM health_weight_logs
            WHERE user_id = ?
            ORDER BY date DESC, id DESC
            LIMIT 1;
            """,
            (user["id"],),
        ).fetchone()

        today_nutrition = connection.execute(
            """
            SELECT *
            FROM health_nutrition_logs
            WHERE user_id = ?
              AND date = ?
            LIMIT 1;
            """,
            (user["id"], today_iso()),
        ).fetchone()

        if weight_goal:
            start_weight = weight_goal["start_value"]
            goal_weight = weight_goal["target_value"]
            current_weight = latest_weight["weight_kg"] if latest_weight else weight_goal["current_value"]
            progress = calculate_progress(start_weight, current_weight, goal_weight)
        else:
            start_weight = None
            current_weight = latest_weight["weight_kg"] if latest_weight else None
            goal_weight = None
            progress = 0

        return {
            "user_name": user["name"],
            "current_weight": current_weight,
            "start_weight": start_weight,
            "goal_weight": goal_weight,
            "weight_progress": progress,
            "calories": today_nutrition["calories"] if today_nutrition else None,
            "protein": today_nutrition["protein_g"] if today_nutrition else None,
        }

    finally:
        connection.close()