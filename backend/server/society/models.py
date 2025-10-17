from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Clan(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255)
    wifi_password = models.CharField(max_length=100, blank=True, null=True)
    owner_telephone = models.CharField(max_length=20, blank=True, null=True)
    owner_email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Clans"
        ordering = ['name']

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE, related_name='memberships')
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        unique_together = ('user', 'clan','joined_at')
    def __str__(self):
        return f"{self.user.username} - {self.clan.name}"

class ClanRule(models.Model):
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE, related_name='rules')
    rule_text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rules')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rule for {self.clan.name}: {self.rule_text[:50]}..."  # Show first 50 chars