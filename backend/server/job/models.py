from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth.models import User
from rest_framework import status
from society.models import Clan

from datetime import datetime, timedelta

WORK_PERIOD_CHOICES = {
    "1d"  : "Daily",
    "2d"  : "Each 2 Days",
    "1w"  : "Weekly",
    "2w"  : "Each 2 weeks",
    "1m"  : "Monthly",
    "2m"  : "Each 2 Month",
    "1y"  : "Yearly",
}
NUMBER_OF_DAYS_IN_5_YEARS = 365 * 5
current_datetime = datetime.now()
default_end_datetime = current_datetime + timedelta(days=NUMBER_OF_DAYS_IN_5_YEARS) #current day + 5 years

class Work(models.Model):
    title = models.CharField(max_length=255,
                             null=False,
                             db_comment="Title of each Work-Template.",
                             help_text="Please use less than 255 characters")
    start = models.DateTimeField(default=current_datetime)
    end = models.DateTimeField(default=default_end_datetime)
    period = models.CharField(choices=WORK_PERIOD_CHOICES, max_length=2, default="1d")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_infinite = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL)
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE)
    duration = models.IntegerField(null=False)

    def __self__(self):
        return self.title + self.clan

TASK_PRIORITY = {
    1 : "low",
    2 : "middle",
    3 : "high",
    4 : "very high"
}

class Task(models.Model):
     title = models.CharField(max_length=255,
                             null=False,
                             blank=False,
                             db_comment="Title of each Task",
                             help_text="Please use less than 255 characters")
     work = models.ForeignKey(Work, on_delete=models.CASCADE, null=False, blank=False)
     priority = models.SmallIntegerField(choices=TASK_PRIORITY, validators=[MinValueValidator(1), MaxValueValidator(4)])


     def __self__(self):
         return self.title + self.work.title + self.work.clean

WORK_ASSIGNMENT_STATUS = {
     "a" : "Assigned",
     "u" : "Unassigned",
     "f" : "Finished",
     "n" : "Not Done",
}
class Assignment(models.Model):
      assigned_user   = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
      task   = models.ForeignKey(Task, on_delete=models.CASCADE, null=False, blank=False)
      status = models.CharField(choices=WORK_ASSIGNMENT_STATUS, max_length=1, null=False, blank=False)
      start   = models.DateTimeField(null=False)
      end = models.DateTimeField(null=False)
      finished_by = models.ForeignKey(User, on_delete=models.CASCADE)

      def __self__(self):
           return self.task.title + self.start

class DayOff(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE ,null=False)
     mode = models.CharField(max_length=255, null=False, blank=False )
     date = models.DateField(null=False)

