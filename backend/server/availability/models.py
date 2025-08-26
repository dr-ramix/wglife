from django.db import models

from django.contrib.auth.models import User

MODE_OFF_DAY_OFF = {
     "si":"Sick",
     "nh":"Not at home",
     "do":"Day off",
}

class DayOff(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE ,null=False)
     mode = models.CharField(max_length=2, null=False, blank=False, choices=MODE_OFF_DAY_OFF)
     date = models.DateField(null=False)

