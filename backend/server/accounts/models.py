from django.conf import settings
from django.db import models

class Profile(models.Model):
    """
    User profile model to extend the User model with additional fields.
    """
    GENDER_CHOICES = [
        ('M', 'male'),
        ('F', 'female'),
        ('O', 'other'),
    ]
    #Primary key is set to user_id which is a OneToOneField to the User model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,            #
        related_name='profile',
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    telephone = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"