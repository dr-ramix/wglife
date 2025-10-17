from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import date



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
        User,
        on_delete=models.CASCADE,
        primary_key=True,            #
        related_name='profile',
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    telephone = models.CharField(max_length=30, blank=True, null=True)

    @property
    def has_today_birthday(self) -> bool:
       if self.birth_date:
           today = date.today()
           if self.birth_date.month == today.month and self.birth_date.day == today.day:
               return True
       return False
    
    def __str__(self) -> str:
        return f"{self.user.username}'s Profile"