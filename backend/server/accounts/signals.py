from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_on_user_creation(sender, instance, created, **kwargs):
    """
    Create a Profile instance whenever a User is created.
    """
    if created:
        Profile.objects.create(user=instance)