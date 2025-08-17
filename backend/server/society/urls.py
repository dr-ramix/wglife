from django.urls import path, include
from .views import ClanListCreateAPIView, ClanDetailAPIView

urlpatterns = [
    path("clans/", ClanListCreateAPIView.as_view(), name="clan-list-create"),
    path("clans/<int:pk>/", ClanDetailAPIView.as_view(), name="clan-detail"),
]