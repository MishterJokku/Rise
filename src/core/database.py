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

        today_checkin = connection.execute(
            """
            SELECT *
            FROM daily_checkins
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
            "mood": today_checkin["mood_score"] if today_checkin else None,
            "energy": today_checkin["energy_score"] if today_checkin else None,
            "stress": today_checkin["stress_score"] if today_checkin else None,
            "sleep_hours": today_checkin["sleep_hours"] if today_checkin else None,
        }

    finally:
        connection.close()


def get_today_checkin_data():
    connection = get_connection()
    today = today_iso()

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

        weight_log = connection.execute(
            """
            SELECT *
            FROM health_weight_logs
            WHERE user_id = ?
              AND date = ?
            LIMIT 1;
            """,
            (user["id"], today),
        ).fetchone()

        nutrition_log = connection.execute(
            """
            SELECT *
            FROM health_nutrition_logs
            WHERE user_id = ?
              AND date = ?
            LIMIT 1;
            """,
            (user["id"], today),
        ).fetchone()

        checkin = connection.execute(
            """
            SELECT *
            FROM daily_checkins
            WHERE user_id = ?
              AND date = ?
            LIMIT 1;
            """,
            (user["id"], today),
        ).fetchone()

        mind_log = connection.execute(
            """
            SELECT *
            FROM mind_logs
            WHERE user_id = ?
              AND date = ?
            LIMIT 1;
            """,
            (user["id"], today),
        ).fetchone()

        return {
            "date": today,
            "weight": weight_log["weight_kg"] if weight_log else None,
            "calories": nutrition_log["calories"] if nutrition_log else None,
            "protein": nutrition_log["protein_g"] if nutrition_log else None,
            "mood": checkin["mood_score"] if checkin else (mind_log["mood_score"] if mind_log else None),
            "energy": checkin["energy_score"] if checkin else (mind_log["energy_score"] if mind_log else None),
            "stress": checkin["stress_score"] if checkin else (mind_log["stress_score"] if mind_log else None),
            "sleep_hours": checkin["sleep_hours"] if checkin else (mind_log["sleep_hours"] if mind_log else None),
            "notes": checkin["notes"] if checkin else (mind_log["journal"] if mind_log else ""),
        }

    finally:
        connection.close()


def save_daily_checkin(weight, calories, protein, mood, energy, stress, sleep_hours, notes):
    connection = get_connection()
    timestamp = now_iso()
    today = today_iso()

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
            raise ValueError("A user profile is required before saving a daily check-in.")

        user_id = user["id"]
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO health_weight_logs
            (user_id, date, weight_kg, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, date) DO UPDATE SET
                weight_kg = excluded.weight_kg,
                updated_at = excluded.updated_at;
            """,
            (user_id, today, weight, timestamp, timestamp),
        )

        cursor.execute(
            """
            INSERT INTO health_nutrition_logs
            (user_id, date, calories, protein_g, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id, date) DO UPDATE SET
                calories = excluded.calories,
                protein_g = excluded.protein_g,
                updated_at = excluded.updated_at;
            """,
            (user_id, today, calories, protein, timestamp, timestamp),
        )

        cursor.execute(
            """
            INSERT INTO daily_checkins
            (user_id, date, mood_score, energy_score, stress_score, sleep_hours, notes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id, date) DO UPDATE SET
                mood_score = excluded.mood_score,
                energy_score = excluded.energy_score,
                stress_score = excluded.stress_score,
                sleep_hours = excluded.sleep_hours,
                notes = excluded.notes,
                updated_at = excluded.updated_at;
            """,
            (user_id, today, mood, energy, stress, sleep_hours, notes, timestamp, timestamp),
        )

        cursor.execute(
            """
            INSERT INTO mind_logs
            (user_id, date, mood_score, energy_score, stress_score, sleep_hours, journal, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id, date) DO UPDATE SET
                mood_score = excluded.mood_score,
                energy_score = excluded.energy_score,
                stress_score = excluded.stress_score,
                sleep_hours = excluded.sleep_hours,
                journal = excluded.journal,
                updated_at = excluded.updated_at;
            """,
            (user_id, today, mood, energy, stress, sleep_hours, notes, timestamp, timestamp),
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_checkin_history(limit=30):
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
            return []

        safe_limit = max(1, int(limit))

        rows = connection.execute(
            """
            WITH checkin_dates AS (
                SELECT user_id, date FROM health_weight_logs WHERE user_id = ?
                UNION
                SELECT user_id, date FROM health_nutrition_logs WHERE user_id = ?
                UNION
                SELECT user_id, date FROM daily_checkins WHERE user_id = ?
                UNION
                SELECT user_id, date FROM mind_logs WHERE user_id = ?
            )
            SELECT
                checkin_dates.date,
                weight.weight_kg,
                nutrition.calories,
                nutrition.protein_g,
                COALESCE(checkins.mood_score, mind.mood_score) AS mood_score,
                COALESCE(checkins.energy_score, mind.energy_score) AS energy_score,
                COALESCE(checkins.stress_score, mind.stress_score) AS stress_score,
                COALESCE(checkins.sleep_hours, mind.sleep_hours) AS sleep_hours,
                COALESCE(checkins.notes, mind.journal, '') AS notes
            FROM checkin_dates
            LEFT JOIN health_weight_logs AS weight
                ON weight.user_id = checkin_dates.user_id
               AND weight.date = checkin_dates.date
            LEFT JOIN health_nutrition_logs AS nutrition
                ON nutrition.user_id = checkin_dates.user_id
               AND nutrition.date = checkin_dates.date
            LEFT JOIN daily_checkins AS checkins
                ON checkins.user_id = checkin_dates.user_id
               AND checkins.date = checkin_dates.date
            LEFT JOIN mind_logs AS mind
                ON mind.user_id = checkin_dates.user_id
               AND mind.date = checkin_dates.date
            ORDER BY checkin_dates.date DESC
            LIMIT ?;
            """,
            (user["id"], user["id"], user["id"], user["id"], safe_limit),
        ).fetchall()

        return [
            {
                "date": row["date"],
                "weight": row["weight_kg"],
                "calories": row["calories"],
                "protein": row["protein_g"],
                "mood": row["mood_score"],
                "energy": row["energy_score"],
                "stress": row["stress_score"],
                "sleep_hours": row["sleep_hours"],
                "notes": row["notes"],
            }
            for row in rows
        ]

    finally:
        connection.close()


def get_health_summary():
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

        if weight_goal is None:
            return None

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

        start_weight = weight_goal["start_value"]
        goal_weight = weight_goal["target_value"]
        current_weight = latest_weight["weight_kg"] if latest_weight else weight_goal["current_value"]
        progress = calculate_progress(start_weight, current_weight, goal_weight)

        if current_weight is None or goal_weight is None:
            remaining_weight = None
        elif goal_weight < start_weight:
            remaining_weight = max(0, current_weight - goal_weight)
        else:
            remaining_weight = max(0, goal_weight - current_weight)

        if remaining_weight is not None:
            remaining_weight = round(remaining_weight, 1)

        return {
            "current_weight": current_weight,
            "start_weight": start_weight,
            "goal_weight": goal_weight,
            "weight_progress": progress,
            "remaining_weight": remaining_weight,
            "latest_weight_date": latest_weight["date"] if latest_weight else None,
        }

    finally:
        connection.close()


def get_weight_history(limit=30):
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
            return []

        safe_limit = max(1, int(limit))

        rows = connection.execute(
            """
            SELECT date, weight_kg
            FROM health_weight_logs
            WHERE user_id = ?
            ORDER BY date DESC, id DESC
            LIMIT ?;
            """,
            (user["id"], safe_limit),
        ).fetchall()

        return [
            {
                "date": row["date"],
                "weight": row["weight_kg"],
            }
            for row in rows
        ]

    finally:
        connection.close()
