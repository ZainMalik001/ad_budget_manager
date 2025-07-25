from django.db import models
from django.utils import timezone
from typing import Optional
from uuid import uuid4

class Brand(models.Model):
    id: str = models.CharField(primary_key=True, default=lambda: str(uuid4()), max_length=50)
    name: str = models.CharField(max_length=100)
    daily_budget: float = models.FloatField(default=0.0)
    monthly_budget: float = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return self.name


class Campaign(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active"
        PAUSED = "paused"
        STOPPED = "stopped"

    id: str = models.CharField(primary_key=True, default=lambda: str(uuid4()), max_length=50)
    brand: Brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name: str = models.CharField(max_length=100)
    daily_spend: float = models.FloatField(default=0.0)
    monthly_spend: float = models.FloatField(default=0.0)
    status: str = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    allowed_start_hour: int = models.IntegerField(default=0)
    allowed_end_hour: int = models.IntegerField(default=23)

    def __str__(self) -> str:
        return self.name

    def is_within_schedule(self) -> bool:
        now_hour = timezone.now().hour
        return self.allowed_start_hour <= now_hour <= self.allowed_end_hour
