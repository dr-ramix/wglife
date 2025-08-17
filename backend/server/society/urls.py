from django.urls import path, include
from .views import ClanListCreateAPIView

urlpatterns = [
    path("clans/", ClanListCreateAPIView.as_view(), name="clan-list-create")
]