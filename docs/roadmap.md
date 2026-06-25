# Roadmap

## Purpose

This roadmap defines the development path for Rise.

It exists to keep the project focused, prevent feature creep, and make sure each version delivers real value.

Rise should grow step by step.

The first goal is not to build everything.

The first goal is to build something useful enough to open every day.

---

# Version 0.1 — Foundation MVP

## Goal

Build a usable offline desktop app that helps users start tracking life progress.

## Core Features

* First-time onboarding
* Local user profile
* Offline SQLite database
* Dashboard
* Health module basics
* Weight tracking
* Calorie tracking
* Daily check-in
* Basic progress bars
* Settings page
* Local backup and restore

## Health Module Scope

Version 0.1 Health module should support:

* Current weight
* Goal weight
* Start weight
* Daily weight logs
* Daily calorie logs
* Protein tracking
* Body goal progress bar

## Mind Scope

Version 0.1 Mind tracking should support:

* Mood score
* Energy score
* Sleep hours
* Stress score
* Notes

## Projects Scope

Version 0.1 Projects module should support:

* Project name
* Minutes worked
* XP earned
* Weekly project time

## Success Criteria

Version 0.1 is successful if:

* User can install and open the app.
* User can complete onboarding.
* User can enter daily weight and calories.
* User can complete a daily check-in.
* User can see body goal progress.
* User data is stored locally.
* App works without internet.
* User can export a backup.

---

# Version 0.2 — Progress and History

## Goal

Make progress visible over time.

## Features

* Weight history graph
* Calorie history graph
* Mood history graph
* Energy history graph
* Weekly review
* Monthly review
* Active days tracking
* Milestones
* Basic achievements

## Success Criteria

Version 0.2 is successful if:

* User can see whether they are moving toward or away from goals.
* User can understand weekly progress.
* User can see history without reading raw logs.
* Missing days do not feel punishing.
* The app gives a simple weekly summary.

---

# Version 0.3 — Modular System

## Goal

Convert Rise into a proper modular Life Progress System.

## Features

* Module manager
* Enable or disable modules
* Health module
* Mind module
* Finance module
* Personal Projects module
* Learning module
* Shared progress system
* Module-based dashboard cards

## Success Criteria

Version 0.3 is successful if:

* Dashboard loads active modules dynamically.
* User can choose which life areas matter.
* Modules follow a consistent structure.
* New modules can be added without rewriting the whole app.

---

# Version 0.4 — Roadmap Engine

## Goal

Help users know what to do next.

## Features

* Goal scoring
* Priority system
* Milestone generator
* Next-step recommendation
* Progress-based adjustment
* Missed-progress recovery suggestions
* Rule-based insights

## Success Criteria

Version 0.4 is successful if:

* App can suggest useful next steps.
* Suggestions are based on goals and progress.
* The app adapts without requiring AI.
* User feels less confused about what to do next.

---

# Version 0.5 — Finance and Projects Expansion

## Goal

Expand Rise beyond health into money and personal growth.

## Finance Features

* Emergency fund tracking
* Debt tracking
* Income tracking
* Expense tracking
* Savings goals
* Monthly financial summary

## Projects Features

* Project XP
* Project milestones
* Time spent on projects
* Empire progress view
* Weekly project review

## Success Criteria

Version 0.5 is successful if:

* User can track financial progress.
* User can track personal project progress.
* Dashboard shows multiple life progress areas.
* The user can see how small work sessions build long-term progress.

---

# Version 0.6 — Optional Local AI

## Goal

Add optional local AI support without breaking offline-first principles.

## Features

* Ollama integration
* Local AI insights
* Weekly reflection summaries
* Goal review assistant
* Roadmap review assistant
* No paid API required
* AI can be fully disabled

## Success Criteria

Version 0.6 is successful if:

* Rise still works completely without AI.
* AI runs locally if enabled.
* User data does not leave the machine.
* AI adds insight without becoming the core product.

---

# Future Ideas

These are not part of the MVP.

* Cloud sync
* Mobile companion app
* Plugin marketplace
* Progress photos
* Community modules
* Public goal templates
* Encrypted backups
* Calendar integration
* Wearable integration
* Local network sync
* Digital detox mode
* Focus mode
* Yearly Life Replay

---

# MVP Boundaries

Version 0.1 should not include:

* Cloud sync
* AI
* Mobile app
* Plugin marketplace
* Complex finance tools
* Advanced charts
* Social features
* Online accounts
* Subscription system

These can come later.

The first version should stay small, private, offline, and useful.

---

# Product Rule

Every roadmap item must support at least one of these questions:

> What should I do next?

Or:

> Am I making progress?

If a feature does not support either question, it should be moved to Future Ideas or removed.
