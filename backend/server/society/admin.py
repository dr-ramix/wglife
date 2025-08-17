from django.contrib import admin
from .models import Clan, Membership, ClanRule

admin.site.register(Clan)
admin.site.register(Membership)
admin.site.register(ClanRule)
