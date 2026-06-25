# Database Design

## Purpose

This document defines the first database design for Rise.

Rise uses SQLite because it is simple, fast, offline-first, portable, and stores data locally on the user's computer.

The database should support:

* User profile
* Settings
* Modules
* Goals
* Milestones
* Daily check-ins
* Health tracking
* Mind tracking
* Project tracking
* Finance tracking
* Achievements
* Backup and restore

---

# Database Philosophy

Rise data belongs to the user.

The database should be:

* Local
* Private
* Portable
* Easy to back up
* Easy to restore
* Independent from cloud
* Independent from login
* Independent from internet

No user data should be uploaded by default.

---

# Database File

Development database path:

```text
data/rise.db
```

Future packaged app path:

```text
C:/Users/<User>/AppData/Local/Rise/rise.db
```

The `data/` folder should not be committed to Git.

---

# Core Tables

## users

Stores basic user profile data.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    height_cm REAL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

---

## user_settings

Stores app preferences.

```sql
CREATE TABLE user_settings (
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
```

---

## modules

Stores available modules and whether they are enabled.

```sql
CREATE TABLE modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    enabled INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

Example module keys:

```text
health
mind
finance
projects
learning
relationships
```

---

## goals

Stores user goals across all modules.

```sql
CREATE TABLE goals (
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
```

Example:

```text
module_key: health
title: Reach 65kg
start_value: 72
current_value: 70
target_value: 65
unit: kg
```

---

## milestones

Stores smaller steps inside goals.

```sql
CREATE TABLE milestones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    target_value REAL,
    current_value REAL,
    unit TEXT,
    status TEXT DEFAULT 'active',
    due_date TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (goal_id) REFERENCES goals(id)
);
```

Example:

```text
Goal: Reach 65kg
Milestone 1: Reach 70kg
Milestone 2: Reach 68kg
Milestone 3: Reach 65kg
```

---

## daily_checkins

Stores daily user check-in data.

```sql
CREATE TABLE daily_checkins (
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
```

---

# Health Module Tables

## health_weight_logs

Stores body weight entries.

```sql
CREATE TABLE health_weight_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    weight_kg REAL NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, date)
);
```

---

## health_nutrition_logs

Stores nutrition entries.

```sql
CREATE TABLE health_nutrition_logs (
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
```

---

## health_measurement_logs

Stores body measurements.

```sql
CREATE TABLE health_measurement_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    waist_cm REAL,
    chest_cm REAL,
    arm_cm REAL,
    thigh_cm REAL,
    hip_cm REAL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, date)
);
```

---

# Mind Module Tables

## mind_logs

Stores mood, mental state, and reflection data.

```sql
CREATE TABLE mind_logs (
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
```

---

# Projects Module Tables

## projects

Stores personal, career, or creative projects.

```sql
CREATE TABLE projects (
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
```

---

## project_sessions

Stores time spent on projects.

```sql
CREATE TABLE project_sessions (
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
```

---

# Finance Module Tables

Finance is planned, but not required for the first MVP implementation.

## finance_accounts

Stores finance accounts or categories.

```sql
CREATE TABLE finance_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    account_type TEXT,
    balance REAL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## finance_transactions

Stores income, expenses, debt payments, or savings.

```sql
CREATE TABLE finance_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    category TEXT,
    amount REAL NOT NULL,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## finance_goals

Stores emergency fund, debt, and savings goals.

```sql
CREATE TABLE finance_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    goal_type TEXT,
    target_amount REAL,
    current_amount REAL DEFAULT 0,
    due_date TEXT,
    status TEXT DEFAULT 'active',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

# Achievement Tables

## achievements

Stores available achievements.

```sql
CREATE TABLE achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    achievement_key TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT,
    module_key TEXT,
    xp_reward INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

---

## user_achievements

Stores unlocked achievements.

```sql
CREATE TABLE user_achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    achievement_id INTEGER NOT NULL,
    unlocked_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (achievement_id) REFERENCES achievements(id),
    UNIQUE(user_id, achievement_id)
);
```

---

# Migration System

Rise should support database migrations.

## schema_migrations

Stores applied database migrations.

```sql
CREATE TABLE schema_migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version TEXT NOT NULL UNIQUE,
    description TEXT,
    applied_at TEXT NOT NULL
);
```

Each migration should have:

* Version
* Description
* SQL changes
* Applied timestamp

---

# Backup Design

Rise should support local backup export.

Future backup format:

```text
RiseBackup_YYYY_MM_DD.rise
```

A backup should contain:

* SQLite database
* User settings
* Optional local files
* Export metadata

Backup and restore should work without internet.

---

# Version 0.1 MVP Tables

Version 0.1 should focus only on the minimum useful database.

Required first tables:

* users
* user_settings
* modules
* goals
* daily_checkins
* health_weight_logs
* health_nutrition_logs
* mind_logs
* projects
* project_sessions
* schema_migrations

Finance and achievements can be documented now but implemented later.

---

# Database Rules

* Store dates as ISO text.
* Use SQLite locally.
* Keep user data private.
* Do not require cloud.
* Do not require login.
* Do not commit database files to Git.
* Use migrations for schema changes.
* Keep tables simple at first.
* Expand only when needed.

---

# Final Note

The database should support the product vision without becoming overly complex.

Version 0.1 should be simple, reliable, and easy to back up.
