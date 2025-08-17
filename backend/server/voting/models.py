from django.db import models
from django.contrib.auth.models import User

class Poll(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_polls')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_votes = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def allow_multiple(self) -> bool:
        return self.max_choices > 1

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Polls"
        ordering = ['-created_at']

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.poll.title} - {self.text}"
    class Meta:
        verbose_name_plural = "Poll Options"
        ordering = ['poll__title', 'text']

class PollVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poll_votes')
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='votes')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'option', 'poll')

    def __str__(self):
        return f"{self.user.username} voted for {self.option.text} in {self.poll.title}"
