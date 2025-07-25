Project Overview
This system automatically manages ad campaign budgets and status:

    Tracks daily and monthly spend
    Automatically pauses campaigns exceeding budgets
    Supports dayparting logic
    Resets budgets via scheduled tasks (Celery)

Getting Started
# Create environment
conda create -n adenv python=3.10
conda activate adenv

# Install dependencies
pip install -r requiremnents.txt

# Run Redis
brew services start redis

# Migrate
python manage.py migrate
python manage.py createsuperuser



Run Services
# Run Django
python manage.py runserver

# Run Celery worker
celery -A ad_budget_manager worker --loglevel=info

# Run Celery Beat
celery -A ad_budget_manager beat --loglevel=info


Models Overview
    Brand — stores daily/monthly budget
    Campaign — stores spend, status, schedule
    PeriodicTask — used for Celery scheduling via admin
    
System Daily Workflow
    Every 10 min: check_campaign_spends() auto-pauses campaigns
    At midnight: reset_daily_spends() resets daily budget
    On 1st of month: reset_monthly_spends() resets monthly budget
