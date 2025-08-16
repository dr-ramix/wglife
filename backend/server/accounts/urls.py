from django.urls import path, include
from .views import ProfileListCreateAPIView


urlpatterns = [
    path("profile/", ProfileListCreateAPIView.as_view(), name="profile-list-create"),
    #path('profile/me/'),
    #path('profile/<int:pk>/', ),
]

 