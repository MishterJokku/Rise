# UI Design

## Purpose

This document defines the user interface direction for Rise.

The UI should feel calm, private, clear, and progress-focused.

Rise should not feel like a stressful productivity dashboard.

It should feel like a personal roadmap.

---

# UI Principles

## 1. Calm First

The app should reduce stress.

Use clear spacing, simple cards, readable text, and minimal clutter.

## 2. One Next Step

The user should always know what to do next.

Do not show too many actions at once.

## 3. Visible Progress

Progress should be easy to understand.

Use progress bars, simple percentages, timelines, and summaries.

## 4. Encourage, Never Shame

Avoid guilt-based wording.

Do not say:

> You failed.

Say:

> Welcome back. Let's continue from where you left off.

## 5. Offline and Private

Privacy should be visible in the UI.

Users should understand that their data stays on their computer.

## 6. Modular Layout

The UI should support modules.

Users should only see the life areas they enabled.

---

# Visual Style

Preferred style:

* Dark theme first
* Card-based layout
* Rounded corners
* Calm contrast
* Soft progress bars
* Clear typography
* Minimal animation
* Slight RPG/progress feeling
* Professional, not childish

Rise should feel modern but not distracting.

---

# First-Time Onboarding Flow

## Purpose

Most apps ask users to create habits.

Rise should first ask:

> Who are you trying to become?

The onboarding should understand the user's life situation and create the first roadmap.

The onboarding must feel calm, simple, and personal.

---

# Onboarding Principles

* Keep it short.
* Use simple language.
* Avoid too many fields at once.
* Do not make users feel judged.
* Explain why questions matter.
* Allow optional sections to be skipped.
* Store everything offline.
* No account required.
* No internet required.

---

# Screen 1 — Welcome

## Title

```text
Welcome to Rise
```

## Subtitle

```text
Small steps. Visible progress.
```

## Description

```text
Rise helps you understand where you are, choose what matters, and see your progress over time.

Everything is stored on your computer.

No account required.
```

## Primary Button

```text
Start Building
```

## UI Notes

This screen should immediately communicate privacy and calmness.

The user should feel safe before giving any information.

---

# Screen 2 — Basic Profile

## Question

```text
Let's understand your starting point.
```

## Fields

* Name
* Age
* Height
* Current weight
* Occupation
* Typical wake time
* Typical sleep time

## Helper Text

```text
This helps Rise personalize health, energy, and daily planning suggestions.
```

## Buttons

```text
Back
Continue
```

## Notes

Only name should feel personal.

The rest should feel practical.

Do not make the form feel like a medical questionnaire.

---

# Screen 3 — Life Area Rating

## Question

```text
How satisfied are you with these areas right now?
```

## Sliders

Each slider ranges from 1 to 10.

* Health
* Mind
* Finance
* Career
* Learning
* Relationships
* Personal Projects
* Happiness

## Helper Text

```text
This helps Rise understand which areas need attention first.
```

## Notes

This screen should not judge the user.

Low scores are not failures.

They are starting points.

---

# Screen 4 — Current Struggles

## Question

```text
What feels difficult right now?
```

## Options

* Low motivation
* Financial pressure
* Weight gain
* Poor sleep
* No direction
* Stress
* Lack of consistency
* Too much screen time
* Health issue
* Career confusion
* Other

## Helper Text

```text
This helps Rise suggest realistic first milestones.
```

## Notes

Multiple selections allowed.

This screen helps the app understand the user's current bottlenecks.

---

# Screen 5 — Health Conditions

## Question

```text
Any health context Rise should know?
```

## Options

* NAFLD / fatty liver
* Diabetes
* High blood pressure
* Anxiety
* Depression
* ADHD
* Injury
* None
* Prefer not to say
* Other

## Medical Disclaimer

```text
Rise is not a medical app.

It helps you track progress, but it does not replace professional medical advice.
```

## Notes

This screen must be optional.

The user should never feel forced to share sensitive information.

---

# Screen 6 — Dreams and Goals

## Question

```text
What kind of life are you trying to build?
```

## Options

* Lose fat
* Gain muscle
* Become healthier
* Build emergency fund
* Become debt free
* Start a business
* Improve career
* Learn a skill
* Build personal projects
* Improve happiness
* Improve relationships
* Reduce screen time
* Other

## Notes

Multiple selections allowed.

This is where Rise shifts from tracking to direction.

---

# Screen 7 — Time Availability

## Question

```text
How much time can you realistically invest per day?
```

## Options

* 10 minutes
* 15 minutes
* 30 minutes
* 1 hour
* 2 hours
* It changes daily

## Helper Text

```text
Rise should assign realistic next steps, not impossible plans.
```

## Notes

This prevents the app from overwhelming the user.

Someone with 10 minutes should not receive a 2-hour plan.

---

# Screen 8 — First Roadmap Preview

## Title

```text
Your First 30 Days
```

## Example Roadmap

```text
Health
- Track weight daily
- Stay within calorie target
- Walk or train 3x per week

Mind
- Daily mood and energy check-in
- Sleep tracking

Projects
- 20 minutes of project work, 3x per week

Finance
- Track income and expenses
```

## Buttons

```text
Use This Roadmap
Edit Goals
```

## Notes

This screen should give the user clarity.

The user should feel:

> Okay. I know where to start.

---

# Screen 9 — Privacy Confirmation

## Title

```text
Your data stays with you.
```

## Description

```text
Rise stores your information locally on this computer.

No account is required.

No data is uploaded by default.

Cloud and AI features are optional and disabled by default.
```

## Button

```text
Enter Rise
```

## Notes

This screen reinforces trust.

Privacy should be part of the product experience, not hidden in settings.

---

# MVP Onboarding Scope

Version 0.1 onboarding should include:

* Welcome screen
* Basic profile
* Life area rating
* Main goals
* Health goal setup
* Privacy confirmation
* First dashboard creation

Advanced roadmap generation can be improved later.

---

# Future Onboarding Ideas

Not required for version 0.1:

* AI-generated roadmap
* Full finance assessment
* Full career assessment
* Fitness level assessment
* Progress photo setup
* Personality-based planning
* Module marketplace selection
* Custom module creation

---

# Onboarding Success Criteria

Onboarding is successful if the user feels:

> I finally know what to do next.

The user should not feel overwhelmed, judged, or trapped.

The onboarding should create enough data for the first dashboard without asking unnecessary questions.
---

# Dashboard Wireframe

## Purpose

The dashboard is the main screen users see after onboarding.

It should answer two questions:

> What should I do next?

And:

> Am I making progress?

The dashboard should feel calm, clear, and useful.

It should not feel like a spreadsheet or a stressful productivity board.

---

# Dashboard Philosophy

The dashboard should show only what matters right now.

The user should immediately understand:

* The next best step
* Today's progress
* Current health progress
* Current mind status
* Current project progress
* Whether they are moving forward

The dashboard should encourage action without creating pressure.

---

# Layout Structure

Preferred layout:

```text
Sidebar Navigation     Main Dashboard Area
──────────────────────────────────────────
Dashboard              Greeting
Health                 Next Step Card
Mind                   Daily Check-in
Projects               Module Progress Cards
Finance                Recent Progress
History
Settings
```

---

# Top Greeting Section

## Morning Example

```text
Good Morning, Jishnu

Small steps. Visible progress.
```

## Evening Example

```text
Good Evening, Jishnu

Let's review today.
```

## Notes

The greeting should change based on time of day.

The text should feel personal but not overly motivational.

---

# Main Next Step Card

This is the most important card on the dashboard.

## Example

```text
Next Step

Walk for 15 minutes

Reason:
This keeps your health goal moving forward.

Impact:
+1 Health XP
```

## Purpose

The user should not have to decide from 20 tasks.

Rise should suggest one useful action.

In version 0.1, this can be rule-based.

Example rules:

* If weight goal is active and no activity today, suggest walk.
* If daily check-in is incomplete, suggest check-in.
* If project work is 0 this week, suggest 20 minutes of project work.
* If mood is low, suggest a small recovery action.

---

# Overall Progress Section

Show progress by active module.

## Example

```text
Overall Progress

Health       42%
Mind         36%
Projects     18%
Finance      10%
```

## Important Note

This should represent progress toward the user's own goals.

It should not claim to measure the user's entire life objectively.

---

# Daily Check-in Card

## Fields

* Weight
* Calories
* Protein
* Mood
* Energy
* Sleep
* Stress
* Notes

## Button

```text
Save Today
```

## Notes

This should be quick to complete.

The user should be able to finish the daily check-in in under 2 minutes.

---

# Health Card

## Example

```text
Health

Current Weight: 72.0 kg
Goal Weight: 65.0 kg
Progress: 14%

Calories Today:
1850 / 2000

Protein:
130g / 150g
```

## Progress Bar

```text
72kg                            65kg
██████░░░░░░░░░░░░░░░░
```

## Notes

If the user gains weight, the bar can move backward.

But the message should remain supportive.

Example:

```text
You drifted slightly from the plan.
One good day can put you back on track.
```

---

# Mind Card

## Example

```text
Mind

Mood: 5 / 10
Energy: 4 / 10
Sleep: 6.5 hours
Stress: 7 / 10
```

## Notes

Mind tracking should be simple.

Rise should not diagnose the user.

It should only help the user notice patterns.

---

# Projects Card

## Example

```text
Projects

Rise App:
30 minutes today

XP:
+10

Weekly Project Time:
2.5 hours
```

## Notes

Projects should make long-term creative work visible.

Small sessions should feel meaningful.

---

# Finance Card

Finance can appear in the dashboard design, but full finance implementation is not required in version 0.1.

## Example

```text
Finance

Emergency Fund:
₹5,000 / ₹20,000

Debt Remaining:
₹____
```

## Notes

Finance should eventually help users track stability, not shame them about money.

---

# Streak and Recovery Area

Rise should avoid harsh streak language.

## Good Example

```text
Current rhythm:
5 active days this week
```

## If user missed days

```text
Welcome back.
Let's continue with one small step today.
```

## Avoid

```text
You failed your streak.
```

## Notes

Recovery matters more than perfection.

---

# Quick Navigation

Navigation items:

* Dashboard
* Health
* Mind
* Projects
* Finance
* History
* Settings

## Notes

Use sidebar navigation for desktop.

Later mobile version can use bottom navigation.

---

# Dashboard MVP Scope

Version 0.1 dashboard should include:

* Greeting
* Main next step card
* Daily check-in card
* Health card
* Mind card
* Projects card
* Basic progress bars
* Sidebar navigation
* Settings link

---

# Future Dashboard Ideas

Not required for version 0.1:

* Animated life map
* Achievement popups
* AI summary
* Weekly insights
* Progress photos
* Custom widgets
* Drag-and-drop dashboard cards
* Calendar heatmap
* Yearly life replay

---

# Dashboard Success Criteria

The dashboard is successful if the user opens Rise and feels:

> Okay. I know what to do next.

The dashboard should create clarity.

Not pressure.

Not guilt.

Not confusion.
