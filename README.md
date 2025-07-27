
# Django + Celery Ad Budget Management System

This is a backend system for managing advertising budgets for brands and campaigns using Django, Celery, and Redis. It tracks daily and monthly ad spends, handles automatic campaign toggling based on budgets, supports dayparting, and performs resets.

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ad_budget_manager
```

### 2. Create a Conda Environment

```bash
conda create --name venv python=3.10
conda activate venv
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Redis

Make sure Redis is installed and running:

```bash
brew install redis
brew services start redis
```

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Server & Celery Workers

```bash
# Run Django server
python manage.py runserver

# In a new terminal, run Celery worker
celery -A core worker --loglevel=info

# In another terminal, run Celery beat
celery -A core beat --loglevel=info
```

---

## Data Models Overview

- **Brand**: Has a daily and monthly ad budget.
- **Campaign**: Linked to a brand. Tracks status (running/paused), current spend, and allowed schedule (dayparting).
- **Schedule**: Defines what hours a campaign is allowed to run (dayparting logic).
- **Spend**: Tracks daily and monthly ad spend.

**Relationships**:

- One Brand → Many Campaigns
- One Campaign → One Schedule

---

## Daily System Workflow

1. **Spending Tracker (Runs every 10 mins)**:
   - Checks each campaign’s daily and monthly spend.
   - Pauses the campaign if budget exceeded.

2. **Dayparting Checker (Every 10 mins)**:
   - Pauses campaigns outside their allowed schedule.

3. **Daily Reset (Runs at midnight)**:
   - Resets all daily spends.
   - Reactivates campaigns that were paused due to daily limits.

4. **Monthly Reset (Conditionally run on 1st)**:
   - Resets monthly spends.
   - Reactivates campaigns paused due to monthly limits.

---

## Assumptions / Simplifications

- Campaign spend updates are mocked (no actual ad traffic).
- Monthly resets are triggered within daily reset (no separate cron).
- Dayparting windows are simplified to fixed hours per day.
- Admin panel is used for manual model entry and monitoring.

---

##  Type Checking

Run MyPy for static typing checks:

```bash
mypy . --ignore-missing-imports
```

---

## Admin Panel

Visit: `http://127.0.0.1:8000/admin`  
Use your superuser credentials to login and manage data.

---
