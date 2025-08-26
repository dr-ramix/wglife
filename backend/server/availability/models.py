from django.db import models

from django.contrib.auth.models import User


class DayOff(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE ,null=False)
     mode = models.CharField(max_length=255, null=False, blank=False )
     date = models.DateField(null=False)

