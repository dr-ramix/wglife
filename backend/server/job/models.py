from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from society.models import Clan
class WorkPeriod(models.TextChoices):
    DAILY = "1d", "Daily"
    TWO_DAYS = "2d", "Each 2 Days"
    WEEKLY = "1w", "Weekly"
    TWO_WEEKS = "2w", "Each 2 Weeks"
    MONTHLY = "1m", "Monthly"
    TWO_MONTHS = "2m", "Each 2 Months"
    YEARLY = "1y", "Yearly"


class TaskPriority(models.IntegerChoices):
    LOW = 1, "Low"
    MEDIUM = 2, "Medium"
    HIGH = 3, "High"
    VERY_HIGH = 4, "Very High"


class TemplateStatus(models.TextChoices):
    ACTIVE = "a", "Active"
    DELETED = "d", "Deleted"


class WorkCycleStatus(models.TextChoices):
    COMING = "c", "Coming"
    IN_PROGRESS = "p", "Progress"
    FINISHED = "f", "Finished"
    DELETED = "d", "Deleted"


class TaskStatus(models.TextChoices):
    ASSIGNED = "assigned", "Assigned"
    FINISHED = "finished", "Finished"
    DELAYED = "delayed", "Delayed"
    DELETED = "deleted", "Deleted"


def IN_FIVE_YEARS():
    return timezone.now() + timedelta(days=365 * 5)


class Work(models.Model):
    title = models.CharField(max_length=255,
                             null=False,
                             db_comment="Title of each Work-Template.",
                             help_text="Please use less than 255 characters")
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=IN_FIVE_YEARS)
    period = models.CharField(max_length=2,choices=WorkPeriod.choices, default=WorkPeriod.WEEKLY)
    is_infinite = models.BooleanField(default=False)
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE)
    deadline_duration = models.PositiveIntegerField(null=False,
                                                    default=2,
                                                    db_comment="Each task of this has some deadline duration to be completed ",
                                                    validators=MinValueValidator(1))

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(end__gte=models.F('start')),
                name='work_end_after_start'
            )
        ]

    def __str__(self):
        return self.title + self.clan

TASK_TEMPLATE_PRIORITY = {
    1 : "low",
    2 : "middle",
    3 : "high",
    4 : "very high"
}

TASK_TEMPLATE_STATUS = {
    "a" : "active",
    "d" : "deleted",
}


class TasTemplate(models.Model):
     title = models.CharField(max_length=255,
                             null=False,
                             blank=False,
                             db_comment="Title of each Task",
                             help_text="Please use less than 255 characters")
     work = models.ForeignKey(Work, on_delete=models.CASCADE, null=False, blank=False)
     note = models.TextField(null=True, blank=True)
     priority = models.SmallIntegerField(choices=TASK_TEMPLATE_PRIORITY, validators=[MinValueValidator(1), MaxValueValidator(4)])
     status = models.CharField(choices=TASK_TEMPLATE_STATUS, max_length=1, default="a")
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     def __str__(self):
         return self.title + self.work.title + self.work.clean

WORK_CYCLE_STATUS = {
     "c" : "Coming",
     "p" : "Progress",
     "f" : "Finished",
     "d" : "Deleted",
}
class WorkCycle(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, null=False, blank=False)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)
    status = models.ChoicesField(choices=WORK_CYCLE_STATUS, max_length=1, null=False, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def to_be_done(self) -> bool:
         if self.status == "c" and self.start == (datetime.now().date() + timedelta(days=3)):
            return True
         return False

    def __self__(self):
        return self.work.title + "(" + self.start + self.end + ")"

TASK_STATUS = {
    "assigned" : "Assigned",
    "finished" : "Finished",
    "delayed" : "Delayed",
    "deleted" : "Deleted",
}
class Task(models.Model):
        work_cycle = models.ForeignKey(WorkCycle, on_delete=models.CASCADE, null=False, blank=False)
        status = models.ChoicesField(choices=TASK_STATUS, max_length=10, null=False, blank=False)
        title = models.CharField(max_length=255,
                             null=False,
                             blank=False,
                             db_comment="Title of each Task",
                             help_text="Please use less than 255 characters")
        note = models.TextField(null=True, blank=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        assigned_user   = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="assigned_assignments")
        finished_at = models.DateTimeField(null=True, blank=True)
        finished_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="closed_task_instances")

        work = models.ForeignKey(Work, on_delete=models.CASCADE, null=False, blank=False)
        priority = models.SmallIntegerField(choices=TASK_PRIORITY, validators=[MinValueValidator(1), MaxValueValidator(4)])


        def __str__(self) -> str:
            return self.title + " - " + self.work_cycle.work.title + " (" + self.status + ")"
