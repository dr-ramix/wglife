from django.urls import path, include
from .views import PollListCreate, PollDetail, PollVoteCreate
urlpatterns = [
    path("polls/", PollListCreate.as_view(), name="poll-list-create"),
    path("polls/<int:pk>/", PollDetail.as_view(), name="poll-detail"),
    path("poll-votes/", PollVoteCreate.as_view(), name="poll-vote-create"),
]