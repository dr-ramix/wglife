from django.db import transaction
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.pagination import PageNumberPagination

from django.contrib.auth.models import User
from .models import Profile
from .serializers import ProfileSerializer

class StandardResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class ProfileListCreateAPIView(APIView):
    """
    GET:  /accounts/profile/  -> List all profiles
    POST: /accounts/profile/  -> Create a new profile
    """
    permissions = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        queryset = Profile.objects.select_related('user')

        gender = request.query_params.get("gender")
        grade = request.query_params.get("grade")
        ordering = request.query_params.get("ordering")
        search = request.query_params.get("search")

        # Filter profiles based on query parameters
        if gender:
            queryset = queryset.filter(gender=gender)
        if grade:
            queryset = queryset.filter(grade=grade)
        # Search
        if search:
            queryset = queryset.filter(user__username__icontains=search)
        # Ordering
        if ordering:
            queryset = queryset.order_by(ordering)

        paginator = StandardResultSetPagination()
        result_page = paginator.paginate_queryset(queryset, request)

        serializer = ProfileSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

