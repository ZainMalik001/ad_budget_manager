from celery import shared_task
from django.utils import timezone
from .models import Campaign, Brand
from datetime import datetime

@shared_task
def check_campaign_spends() -> None:
    now = timezone.now()
    campaigns = Campaign.objects.select_related("brand").all()

    for campaign in campaigns:
        if (
            campaign.daily_spend >= campaign.brand.daily_budget or
            campaign.monthly_spend >= campaign.brand.monthly_budget
        ):
            campaign.status = Campaign.Status.PAUSED
            campaign.save()
        elif campaign.status == Campaign.Status.PAUSED and campaign.is_within_schedule():
            # Resume if within time window and under budget
            campaign.status = Campaign.Status.ACTIVE
            campaign.save()


@shared_task
def reset_daily_spends() -> None:
    Campaign.objects.all().update(daily_spend=0.0)


@shared_task
def reset_monthly_spends() -> None:
    if timezone.now().day == 1:
        Campaign.objects.all().update(monthly_spend=0.0)
