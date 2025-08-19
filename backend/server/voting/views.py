from django.db import transaction, IntegrityError
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import PollVote, Poll, PollOption
from .serializers import PollSerializer, PollOptionSerializer, PollVoteSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class StandardResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class PollListCreatAPIView(APIView):
    """
    GET: /voting/polls/  -> List all polls
    POST /voting/polls/  -> Create new poll
    """

    permissions = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        queryset = Poll.objects.all()
        paginator = self.pagination_class()
        paged_queryset = paginator.paginate_queryset(queryset, request, view=self)
        serializer = PollSerializer(paged_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request): 
        serializers = PollSerializer(data=request.data)
        if serializers.is_valid():
            try:
                with transaction.atomic():
                    serializers.save()
            except IndentationError:
                return Response({"detail": "Poll creation has been failed due to integrity error."}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class PollDetailAPIView(APIView):
    """
    GET:
    PUT:
    PATCH:
    DELETE:
    """
    def get(self, request, id):
        poll = get_object_or_404(Poll, id=id)
        serializer = PollSerializer(poll)
        return Response(serializer)

    def put(self, request, id):
        poll = get_object_or_404(Poll, id=id)
        serializer = PollSerializer(poll, data = request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_200_OK)
            except IntegrityError:
                    return Response({"detail": "Poll update failed due to integrity error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        poll = get_object_or_404(Poll, id=id)
        serializer = PollSerializer(poll, data = request.data, partial=True)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_200_OK)
            except IntegrityError:
                    return Response({"detail": "Poll update failed due to integrity error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        poll = get_object_or_404(Poll, id=id)
        poll.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class PollVoteListCreate(APIView):
    """

    """
    def get(self, request):
        #####

    def post(self, request):
        request