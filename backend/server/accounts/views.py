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

from django.db.models import Q
class StandardResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class ProfileListCreateAPIView(APIView):
    """
    GET:  /accounts/profiles/  -> List all profiles
    GET:  /accounts/profiles?gender= -> Filter profiles by gender
    GET:  /accounts/profiles?grade=   -> Filter profiles by grade
    GET:  /accounts/profiles?ordering= -> Order profiles by a field
    GET:  /accounts/profiles?search=  -> Search profiles by username, email, first name, or last name
    POST: /accounts/profiles/  -> Create a new profile
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
            queryset = queryset.filter(
                Q(user__username__icontains=search) |
                Q(user__email__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
            )
        # Ordering
        if ordering:
            queryset = queryset.order_by(ordering)

        paginator = StandardResultSetPagination()
        result_page = paginator.paginate_queryset(queryset, request)

        serializer = ProfileSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                profile = serializer.save(user=request.user)
            return Response(ProfileSerializer(profile).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDetailAPIView(APIView):
    """
    GET:  /accounts/profiles/<int:pk>/  -> Retrieve a profile by ID
    PUT:  /accounts/profiles/<int:pk>/  -> Update a profile by ID
    PATCH: /accounts/profiles/<int:pk>/  -> Partially update a profile by ID
    DELETE: /accounts/profiles/<int:pk>/  -> Delete a profile by ID
    """
    permissions = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        profile = get_object_or_404(Profile.objects.select_related('user'), pk=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk):
        profile = get_object_or_404(Profile.objects.select_related('user'), pk=pk)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                updated_profile = serializer.save()
            return Response(ProfileSerializer(updated_profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        profile = get_object_or_404(Profile.objects.select_related('user'), pk=pk)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                updated_profile = serializer.save()
            return Response(ProfileSerializer(updated_profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        profile = get_object_or_404(Profile.objects.select_related('user'), pk=pk)
        user = get_object_or_404(User, pk=pk)
        user.delete()
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProfileCurrentUserAPIView(APIView):
    """
    GET:  /accounts/profiles/me/  -> Retrieve the current user's profile
    PUT:  /accounts/profiles/me/  -> Update the current user's profile
    PATCH: /accounts/profiles/me/  -> Partially update the current user's profile
    DELETE: /accounts/profiles/me/  -> Delete the current user's profile
    """
    permissions = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        profile = get_object_or_404(Profile.objects.select_related('user'), user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = get_object_or_404(Profile.objects.select_related('user'), user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                updated_profile = serializer.save()
            return Response(ProfileSerializer(updated_profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        profile = get_object_or_404(Profile.objects.select_related('user'), user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                updated_profile = serializer.save()
            return Response(ProfileSerializer(updated_profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        profile = get_object_or_404(Profile.objects.select_related('user'), user=request.user)
        user = get_object_or_404(User, pk=request.user.pk)
        profile.delete()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)