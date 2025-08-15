from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    User profile model to extend the default User model with additional fields.
    """
    GENDER_CHOICES = [
        ('M','male'),
        ('F','female'),
        ('O','other'),
    ]
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
