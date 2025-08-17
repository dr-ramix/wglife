from django.urls import path, include

from .views import (ClanListCreateAPIView, ClanDetailAPIView,
                    MyClansListCreateAPIView, MyClansDetailAPIView,
                    MembershipsListCreateAPIView, MembershipDetailAPIView,
                    ClanRulesListCreateAPIView, ClanRuleDetailAPIView)

urlpatterns = [
    path("clans/", ClanListCreateAPIView.as_view(), name="clan-list-create"),
    path("clans/<int:pk>/", ClanDetailAPIView.as_view(), name="clan-detail"),
    path("my-clans/", MyClansListCreateAPIView.as_view(), name="my-clans"),
    path("my-clans/<int:pk>/", MyClansDetailAPIView.as_view(), name="my-clan-detail"),
    path("memberships/", MembershipsListCreateAPIView.as_view(), name="membership-list-create"),
    path("memberships/<int:pk>/", MembershipDetailAPIView.as_view(), name="membership-detail"),
    path("clan-rules/", ClanRulesListCreateAPIView.as_view(), name="clan-rule-list-create"),
    path("clan-rules/<int:pk>/", ClanRuleDetailAPIView.as_view(), name="clan-rule-detail"),
]