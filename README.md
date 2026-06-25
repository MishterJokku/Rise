# Rise

**Small steps. Visible progress.**

Rise is an offline-first Life Progress System that helps users understand where they are, choose what matters, and make visible progress across different areas of life.

Rise is not just a habit tracker.

It is designed to answer two simple questions:

> What should I do next?

And:

> Am I making progress?

---

## Why Rise Exists

Many people do not need more motivation.

They need clarity.

Most people already know they want to become healthier, financially stable, more skilled, more consistent, or more fulfilled. The difficult part is knowing what to do today and seeing whether those small actions are actually moving life forward.

Rise helps users turn vague life goals into clear milestones, daily next steps, and visible progress.

---

## Core Philosophy

Rise is built around these principles:

* Offline first
* Privacy first
* User-owned data
* No account required
* No cloud required
* No tracking by default
* AI is optional
* Progress over perfection
* Encourage, never shame
* Modules, not clutter

Your life data belongs to you.

Rise stores data locally on your computer by default.

---

## What Rise Is

Rise is a modular Life Progress System.

It helps users track and improve areas such as:

* Health
* Mind
* Finance
* Career
* Learning
* Relationships
* Personal Projects
* Hobbies

Each area can become a module with its own goals, milestones, progress cards, achievements, and insights.

---

## What Rise Is Not

Rise is not:

* A basic habit tracker
* A to-do list app
* A cloud-first productivity app
* A motivation quote app
* An AI chatbot
* A Notion clone
* A fitness-only app
* A finance-only app

Rise should reduce overwhelm, not add more pressure.

---

## Version 0.1 Goal

The first version of Rise focuses on building a usable offline desktop app.

### Planned MVP Features

* First-time onboarding
* Local user profile
* Offline SQLite database
* Dashboard
* Health module basics
* Weight tracking
* Calorie tracking
* Daily check-in
* Basic progress bars
* Backup and restore
* Settings page

The goal is not to build everything immediately.

The goal is to build something useful enough to open every day.

---

## Offline-First Approach

Rise should work without internet.

The app should not require:

* Login
* Account creation
* Cloud database
* Online API
* Paid AI service
* Internet connection

Future cloud sync may be added as an optional feature, but it should never be required.

---

## Optional AI

Rise should work fully without AI.

Future AI support may include local AI through tools like Ollama, but AI should remain optional.

The core app must be useful without any paid API.

---

## Tech Stack

Planned stack:

* Python
* PySide6 / Qt
* SQLite
* PyInstaller
* Git + GitHub

---

## Project Structure

```text
Rise/
│
├── docs/
├── src/
│   ├── core/
│   ├── ui/
│   ├── modules/
│   ├── services/
│   └── database/
│
├── tests/
├── scripts/
├── assets/
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Development Roadmap

### Version 0.1 — Foundation MVP

* Onboarding
* Dashboard
* Local database
* Health tracking
* Daily check-in
* Backup and restore

### Version 0.2 — Progress and History

* Graphs
* Weekly review
* Monthly review
* Streaks
* Milestones
* Achievements

### Version 0.3 — Modular System

* Module manager
* Health module
* Mind module
* Finance module
* Projects module
* Learning module

### Version 0.4 — Roadmap Engine

* Goal scoring
* Priority system
* Milestone generator
* Next-step recommendation

### Version 0.5 — Optional Local AI

* Local AI insights
* Ollama support
* Private weekly summaries
* No required paid API

---

## Product Principle

If a feature does not help the user answer one of these questions, it does not belong in Rise:

> What should I do next?

> Am I making progress?

---

## Status

Rise is currently in early development.

This repository is being built step by step with a focus on clean architecture, offline-first design, and long-term modular growth.
