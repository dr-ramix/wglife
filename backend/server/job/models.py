from django.db import models

from django.contrib.auth.models import User
from society.models import Clan



WORK_PERIOD_CHOICES = {
    "1d"  : "Daily",
    "2d"  : "Each 2 Days",
    "1w"  : "Weekly",
    "2w"  : "Each 2 weeks",
    "1m"  : "Monthly",
    "2m"  : "Each 2 Month",
    "1y"  : "Yearly",
}

current_datetime = datetime.datetime.now()

class Work(models.Model):
    title = models.CharField(max_length=255,
                             null=False,
                             db_comment="Title of each Work-Template.",
                             help_text="Please use less than 255 characters")
    start = models.DateTimeField(default=current_datetime)
    end = models.DateTimeField()
    period = models.CharField(choices=WORK_PERIOD_CHOICES, max_length=2, default="1d")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_infinite = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL)
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE)
