from django.db import models

# Create your models here.

class Society(models.Model):
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
        verbose_name_plural = "Societies"
        ordering = ['name']

class Membership(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='memberships')
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='memberships')
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        unique_together = ('user', 'society','joined_at')
    def __str__(self):
        return f"{self.user.username} - {self.society.name}"

class SocietyRule(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='rules')
    rule_text = models.TextField()
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='created_rules')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rule for {self.society.name}: {self.rule_text[:50]}..."  # Show first 50 chars