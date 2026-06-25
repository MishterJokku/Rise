# Architecture

## Purpose

This document defines the technical architecture of Rise.

Rise is an offline-first, modular desktop application designed to help users track progress across different areas of life.

The architecture should support:

* Local data storage
* Privacy-first design
* Modular expansion
* Future backup and restore
* Future optional local AI
* Clean long-term maintainability

---

# Core Architecture

Rise is built around three major layers:

```text
User Interface
↓
Application Core
↓
Local Database
```

## 1. User Interface Layer

The UI layer handles what the user sees and interacts with.

Responsibilities:

* Main window
* Dashboard
* Onboarding
* Settings
* Module screens
* Forms
* Cards
* Charts
* Navigation

The UI should not contain heavy business logic.

---

## 2. Application Core Layer

The core layer handles the main application logic.

Responsibilities:

* App startup
* Configuration
* Settings
* Database connection
* Backup and restore
* Module loading
* Progress calculation
* Goal handling
* Roadmap logic
* Shared services

The core layer should remain independent from individual modules as much as possible.

---

## 3. Local Database Layer

The database layer handles storage.

Rise uses SQLite for offline-first local storage.

Responsibilities:

* Creating database tables
* Running migrations
* Reading data
* Writing data
* Updating data
* Exporting backup data
* Importing restored data

The database should be local by default.

No server should be required.

---

# Offline-First Design

Rise must work without internet.

The app should not require:

* Login
* Account creation
* Cloud database
* Online API
* Paid AI service
* Internet connection

All core data should be stored on the user's machine.

Future cloud sync may be added, but it must be optional.

---

# Proposed Tech Stack

## Language

Python

## Desktop UI

PySide6 / Qt

## Database

SQLite

## Charts

PyQtGraph or Matplotlib

## Packaging

PyInstaller

## Version Control

Git + GitHub

---

# Project Structure

```text
Rise/
│
├── docs/
│   ├── vision.md
│   ├── constitution.md
│   ├── roadmap.md
│   ├── architecture.md
│   ├── database.md
│   ├── modules.md
│   ├── ui.md
│   └── decisions.md
│
├── src/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── app.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── settings.py
│   │   └── backup.py
│   │
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── dashboard.py
│   │   ├── onboarding.py
│   │   └── components/
│   │
│   ├── modules/
│   │   ├── health/
│   │   ├── mind/
│   │   ├── finance/
│   │   ├── projects/
│   │   └── learning/
│   │
│   ├── services/
│   │   ├── progress_engine.py
│   │   ├── roadmap_engine.py
│   │   ├── milestone_engine.py
│   │   └── achievement_engine.py
│   │
│   ├── database/
│   │   └── migrations.py
│   │
│   └── assets/
│
├── tests/
├── scripts/
├── assets/
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Core System

The core system should handle:

* Starting the application
* Loading configuration
* Creating or opening the local database
* Running migrations
* Loading enabled modules
* Managing user settings
* Managing backup and restore
* Providing shared services to modules

The core system should not be tightly tied to one module.

---

# Module System

Rise should grow through modules.

Examples:

* Health
* Mind
* Finance
* Projects
* Learning
* Relationships
* Hobbies

Each module should manage its own area of life.

A module may provide:

* Goals
* Milestones
* Daily check-in fields
* Dashboard cards
* Charts
* Achievements
* Insights
* Suggested next steps

---

# Module Interface

Each module should eventually follow a common interface.

Example:

```python
class BaseModule:
    module_key = "health"
    name = "Health"

    def get_dashboard_cards(self):
        pass

    def get_daily_checkin_fields(self):
        pass

    def get_goals(self):
        pass

    def get_progress_summary(self):
        pass

    def get_suggestions(self):
        pass
```

This allows the dashboard to load module content dynamically.

---

# Dashboard Architecture

The dashboard should not hardcode every life area.

Instead:

```text
Dashboard
↓
Load enabled modules
↓
Ask each module for cards
↓
Display cards
```

This makes Rise easier to expand later.

---

# Data Storage

Rise uses SQLite.

Default development database path:

```text
data/rise.db
```

Future packaged app database path may be:

```text
C:/Users/<User>/AppData/Local/Rise/rise.db
```

All user data should remain local by default.

---

# Backup Architecture

Rise should eventually support local backup export.

Backup file example:

```text
RiseBackup_YYYY_MM_DD.rise
```

A backup should contain:

* SQLite database
* Settings
* Optional local files
* Export metadata

Backup and restore should not require internet.

---

# AI Architecture

AI is not part of Version 0.1.

Future AI support should be optional.

Preferred future AI flow:

```text
Rise
↓
Local SQLite Data
↓
Local AI through Ollama
↓
Private Insight
```

Rules:

* AI must not be required.
* Paid AI APIs must not be required.
* Local AI should be preferred.
* User data should not leave the machine without explicit permission.

---

# Version 0.1 Architecture Scope

Version 0.1 should only implement the minimum foundation:

* App startup
* Main window
* Local SQLite connection
* Basic settings
* Onboarding placeholder
* Dashboard placeholder
* Health data storage
* Daily check-in storage

Do not build advanced AI, cloud, marketplace, or plugin systems in v0.1.

Design for them, but do not implement them yet.

---

# Architecture Principles

Rise architecture should follow these principles:

* Offline first
* Privacy first
* Local data ownership
* Modular expansion
* Simple backup
* No forced cloud
* No forced AI
* Clean separation of concerns
* Easy testing
* Long-term maintainability

---

# Final Rule

The architecture should make the app easier to grow, not harder.

If an architectural decision adds complexity without helping Rise become more private, modular, reliable, or useful, avoid it.
