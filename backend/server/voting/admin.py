from django.contrib import admin

# Register your models here.

from .models import Poll, PollOption, PollVote
admin.site.register(Poll)
admin.site.register(PollOption)
admin.site.register(PollVote)