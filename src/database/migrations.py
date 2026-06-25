from datetime import datetime


def now_iso():
    return datetime.now().isoformat(timespec="seconds")


def run_migrations(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT NOT NULL UNIQUE,
            description TEXT,
            applied_at TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            height_cm REAL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            theme TEXT DEFAULT 'dark',
            offline_mode_enabled INTEGER DEFAULT 1,
            ai_enabled INTEGER DEFAULT 0,
            backup_enabled INTEGER DEFAULT 1,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            description TEXT,
            enabled INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            module_key TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            goal_type TEXT,
            start_value REAL,
            current_value REAL,
            target_value REAL,
            unit TEXT,
            start_date TEXT,
            target_date TEXT,
            status TEXT DEFAULT 'active',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            mood_score INTEGER,
            energy_score INTEGER,
            stress_score INTEGER,
            sleep_hours REAL,
            notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, date)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_weight_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            weight_kg REAL NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, date)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_nutrition_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            calories INTEGER,
            protein_g REAL,
            carbs_g REAL,
            fat_g REAL,
            water_liters REAL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, date)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mind_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            mood_score INTEGER,
            energy_score INTEGER,
            stress_score INTEGER,
            motivation_score INTEGER,
            sleep_hours REAL,
            journal TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, date)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            status TEXT DEFAULT 'active',
            xp INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS project_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            minutes_spent INTEGER NOT NULL,
            notes TEXT,
            xp_earned INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        );
    """)

    cursor.execute(
        """
        INSERT OR IGNORE INTO schema_migrations
        (version, description, applied_at)
        VALUES (?, ?, ?);
        """,
        (
            "0001",
            "Create MVP database tables",
            now_iso(),
        ),
    )


def seed_default_modules(connection):
    cursor = connection.cursor()

    modules = [
        (
            "health",
            "Health",
            "Track weight, calories, protein, and body progress.",
            1,
        ),
        (
            "mind",
            "Mind",
            "Track mood, energy, sleep, stress, and daily reflections.",
            1,
        ),
        (
            "projects",
            "Projects",
            "Track personal projects, work sessions, XP, and progress.",
            1,
        ),
        (
            "finance",
            "Finance",
            "Track emergency fund, debt, savings, income, and expenses.",
            0,
        ),
    ]

    timestamp = now_iso()

    for module_key, name, description, enabled in modules:
        cursor.execute(
            """
            INSERT OR IGNORE INTO modules
            (module_key, name, description, enabled, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            (
                module_key,
                name,
                description,
                enabled,
                timestamp,
                timestamp,
            ),
        )