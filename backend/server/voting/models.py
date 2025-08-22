from django.db import models
from django.contrib.auth.models import User
from rest_framework.fields import ChoiceField
from django.db.models.functions import Now

#Add one more table so we can create same poll for multiple times

STATUS_OF_POLL = [
    ("co", "Completed"),
    ("pe", "Pending"),
    ("ip", "In Progress"),
    ("de", "Deleted"),
    ("in", "Invalid")
]
class Poll(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_polls')
    start_date = models.DateTimeField(db_default=Now())
    end_date = models.DateTimeField()
    max_votes = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=2, choices=STATUS_OF_POLL, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self) -> bool:
        return not ((self.status == "in") or (self.status == "de"))
    
    @property
    def allow_multiple(self) -> bool:
        return self.max_choices > 1

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Polls"
        ordering = ['created_at']

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.poll.title} - {self.text}"
    class Meta:
        verbose_name_plural = "Poll Options"
        ordering = ['created_at']

class PollVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='votes')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'option', 'poll')
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username} voted for {self.option.text} in {self.poll.title}"
