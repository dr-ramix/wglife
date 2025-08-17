from django.shortcuts import render
from django.db import transaction, IntegrityError
from django.db.models import Exists, OuterRef
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from .models import Clan, Membership, ClanRule
from .serializers import ClanSerializer, MembershipSerializer, ClanRuleSerializer
from django.shortcuts import get_object_or_404


class StandardResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ClanListCreateAPIView(APIView):
    """
    GET:   /society/clans/  -> List all clans
    GET:   /society/clans?country= -> Filter clans by country
    GET:   /society/clans?city=   -> Filter clans by city
    GET:   /society/clans?name=   -> Search clans by name
    GET:   /society/clans?order-by= -> Order clans by a field
    POST:  /society/clans/  -> Create a new clan
    """

    permission_classes = [permissions.IsAuthenticated]  # <-- was `permissions`; DRF expects `permission_classes`
    authentication_classes = [JWTAuthentication]
    pagination_class = StandardResultSetPagination
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request):
        queryset = Clan.objects.all()

        country  = request.query_params.get("country")
        city     = request.query_params.get("city")
        search     = request.query_params.get("search")
        order_by = request.query_params.get("order-by")

        if country:
            queryset = queryset.filter(country=country)
        if city:
            queryset = queryset.filter(city=city)
        if search:
            queryset = queryset.filter(name__icontains=search)
        if order_by:
            queryset = queryset.order_by(order_by)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = ClanSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


    def post(self, request):
        serializers = ClanSerializer(data=request.data)
        if serializers.is_valid():
           try:
               with transaction.atomic():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
           except IntegrityError:
               return Response({"detail": "Clan creation failed due to integrity error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ClanDetailAPIView(APIView):
    """
    GET:   /society/clans/<id>/  -> Retrieve a clan by ID
    PUT:   /society/clans/<id>/  -> Update a clan by ID
    PATCH: /society/clans/<id>/  -> Partially update a clan by ID
    DELETE: /society/clans/<id>/  -> Delete a clan by ID
    """
    permissions = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, id):
        clan = get_object_or_404(Clan, id=id)
        serializer = ClanSerializer(clan)
        return Response(serializer.data)

    def put(self, request, id):
        clan = get_object_or_404(Clan, id=id)
        serializer = ClanSerializer(clan, data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response({"detail": "Clan update failed due to integrity error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        clan = get_object_or_404(Clan, id=id)
        serializer = ClanSerializer(clan, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
            except IntegrityError:
                return Response({"detail": "Clan update failed due to integrity error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        clan = get_object_or_404(Clan, id=id)
        clan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MyClansListCreateAPIView(APIView):
    """
    GET: /society/my-clan/  ->  List all clans the current user is a member of
    GET: /society/my-clan/?is-active=true  -> List active clans
    GET: /society/my-clan/?is-active=false -> List inactive clans
    POST: /society/my-clan/  -> Create a new clan + current user as member
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
       user = request.user
       memberships = Membership.objects.filter(user=user)
       is_active = request.query_params.get("is-active")

       if is_active == "true":
            memberships =memberships.filter(user=request.user, is_active=True)
       elif is_active == "false":
            memberships = memberships.filter(user=request.user, is_active=False)

       clan_ids = memberships.values_list('clan_id', flat=True)

       clans = Clan.objects.filter(id__in=clan_ids)
       serializer = ClanSerializer(clans, many=True)
       return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = ClanSerializer(data=data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    clan = serializer.save()
                    Membership.objects.create(user=user, clan=clan, is_active=True)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"detail": "Clan creation failed due to integrity error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyClansDetailAPIView(APIView):
    """
    GET: /society/my-clan/<int:pk>/  -> Retrieve a clan by ID where the current user is a member
    PUT: /society/my-clan/<int:pk>/  -> Update a clan by ID where the current user is a member
    DELETE: /society/my-clan/<int:pk>/  -> Delete a clan by ID where the current user is a member
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        user = request.user
        membership = get_object_or_404(Membership, user=user, clan_id=pk, is_active=True)
        clan = membership.clan
        serializer = ClanSerializer(clan)
        return Response(serializer.data)

    def put(self, request, pk):
        user = request.user
        membership = get_object_or_404(Membership, user=user, clan_id=pk, is_active=True)
        clan = membership.clan
        serializer = ClanSerializer(clan, data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response({"detail": "Clan update failed due to integrity error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = request.user
        membership = get_object_or_404(Membership, user=user, clan_id=pk, is_active=True)
        clan = membership.clan
        serializer = ClanSerializer(clan, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response({"detail": "Clan update failed due to integrity error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = request.user
        membership = get_object_or_404(Membership, user=user, clan_id=pk, is_active=True)
        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

