from django.urls import path, include
from .views import ProfileListCreateAPIView, ProfileDetailAPIView, ProfileCurrentUserAPIView


urlpatterns = [
    path("profiles/", ProfileListCreateAPIView.as_view(), name="profile-list-create"),
    path('profiles/me/', ProfileCurrentUserAPIView.as_view(), name="profile-current-user"),
    path('profiles/<int:pk>/', ProfileDetailAPIView.as_view(), name="profile-detail"),
]

