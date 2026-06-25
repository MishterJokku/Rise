# Module System

## Purpose

This document defines how modules work in Rise.

Rise should be modular from the beginning so the app can grow without becoming messy or overwhelming.

The module system allows users to enable only the areas of life they care about.

---

# Module Philosophy

Rise should not force every user to track everything.

A user may care about health and money.

Another user may care about learning and career.

Another user may care about mental health and relationships.

Rise should adapt to the user.

The app should provide modules that can be enabled, disabled, expanded, or improved over time.

---

# Rise Core vs Modules

## Rise Core

Rise Core handles the foundation of the app.

Core responsibilities:

* App startup
* User profile
* Settings
* Local database
* Backup and restore
* Dashboard shell
* Module loading
* Progress engine
* Roadmap engine
* Theme system
* Navigation

## Modules

Modules handle specific life areas.

Examples:

* Health
* Mind
* Finance
* Projects
* Learning
* Career
* Relationships
* Hobbies

Each module should manage its own goals, data, progress cards, and suggestions.

---

# Core Structure

```text
Rise Core
│
├── Health Module
├── Mind Module
├── Finance Module
├── Projects Module
├── Learning Module
├── Relationships Module
└── Custom Modules
```

The dashboard should not hardcode every module.

Instead, the dashboard should load enabled modules and ask them what to display.

---

# What Every Module Can Provide

Each module may provide:

* Goals
* Milestones
* Daily check-in fields
* Dashboard cards
* Data entry forms
* Charts
* Statistics
* Achievements
* Suggestions
* Weekly review content
* Monthly review content

Not every module needs every feature in version 0.1.

The system should support these possibilities over time.

---

# Module Metadata

Each module should have metadata.

Example:

```text
module_key: health
name: Health
description: Track weight, calories, sleep, fitness, and body progress.
enabled: true
version: 0.1.0
```

Required metadata:

* module_key
* name
* description
* enabled
* version

The `module_key` should be stable and lowercase.

Examples:

```text
health
mind
finance
projects
learning
relationships
```

---

# Module Folder Structure

Example module folder:

```text
src/modules/health/
│
├── __init__.py
├── module.py
├── models.py
├── service.py
├── ui.py
└── achievements.py
```

## module.py

Defines the module class and metadata.

## models.py

Defines module-specific data structures.

## service.py

Handles module logic.

## ui.py

Contains module-specific UI screens or cards.

## achievements.py

Defines module-specific achievements.

---

# Base Module Interface

Each module should eventually follow a common interface.

```python
class BaseModule:
    module_key = "example"
    name = "Example Module"
    description = "Module description"
    version = "0.1.0"

    def get_dashboard_cards(self):
        return []

    def get_daily_checkin_fields(self):
        return []

    def get_goals(self):
        return []

    def get_progress_summary(self):
        return {}

    def get_suggestions(self):
        return []
```

This allows Rise Core to communicate with modules in a predictable way.

---

# Dashboard Integration

Dashboard flow:

```text
Dashboard
↓
Load enabled modules
↓
Ask each module for dashboard cards
↓
Display cards
```

Example:

```text
Health Module → Weight progress card
Mind Module → Mood and energy card
Projects Module → Project XP card
Finance Module → Emergency fund card
```

This keeps the dashboard flexible.

---

# Daily Check-in Integration

Each module can provide check-in fields.

Example:

## Health Module

* Weight
* Calories
* Protein
* Water

## Mind Module

* Mood
* Energy
* Stress
* Sleep
* Notes

## Projects Module

* Project worked on
* Minutes spent
* Notes

The daily check-in screen can combine fields from enabled modules.

---

# Goals and Milestones

Each module can create goals.

Example:

## Health Goal

```text
Reach 65kg
```

Milestones:

```text
Reach 70kg
Reach 68kg
Reach 65kg
```

## Finance Goal

```text
Build ₹20,000 emergency fund
```

Milestones:

```text
Save ₹5,000
Save ₹10,000
Save ₹15,000
Save ₹20,000
```

## Projects Goal

```text
Build Rise v0.1
```

Milestones:

```text
Create docs
Build dashboard
Add database
Add health module
Create release build
```

---

# Version 0.1 Modules

For the MVP, only these modules are required.

## Health Module

Tracks:

* Current weight
* Goal weight
* Start weight
* Daily weight logs
* Calories
* Protein
* Body goal progress

## Mind Module

Tracks:

* Mood
* Energy
* Stress
* Sleep
* Notes

## Projects Module

Tracks:

* Project name
* Minutes worked
* XP earned
* Weekly project time

## Finance Module

Finance can be designed and documented, but does not need full implementation in v0.1.

---

# Future Modules

Possible future modules:

* Finance
* Learning
* Career
* Relationships
* Digital wellbeing
* Gaming balance
* Reading
* Meditation
* Custom user-created modules
* Running
* Language learning
* Exam preparation
* Freelancing
* Business building

---

# Plugin Vision

In the long term, Rise may support community modules.

Example:

```text
Rise Module Library
│
├── Running Module
├── IELTS Study Module
├── ADHD Focus Module
├── Pregnancy Module
├── Freelance Business Module
├── Guitar Practice Module
└── Digital Detox Module
```

This is not part of version 0.1.

For now, modules should be internal Python modules.

---

# Module Design Rules

Modules should follow these rules:

* Keep each module focused.
* Do not force users to enable all modules.
* Do not duplicate core logic inside modules.
* Store module data locally.
* Respect offline-first principles.
* Avoid overwhelming the dashboard.
* Each module should provide visible progress.
* Each module should help answer: What should I do next?

---

# Version 0.1 Implementation Rule

Version 0.1 should design for modularity but not overbuild the plugin system.

Do this first:

* Create module folders.
* Create simple module classes.
* Load basic dashboard cards.
* Keep module logic simple.
* Avoid marketplace, dynamic downloads, or external plugins.

Build the foundation now.

Add advanced plugin features later.

---

# Final Note

The module system exists to reduce clutter, not create complexity.

Rise should feel personal because users only see the life areas that matter to them.
