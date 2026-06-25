import sqlite3
from pathlib import Path

from database.migrations import run_migrations, seed_default_modules


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "rise.db"


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