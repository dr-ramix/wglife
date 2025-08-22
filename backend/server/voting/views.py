from django.http import Http404
from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import LimitOffsetPagination

from .models import Poll, PollOption, PollVote
from .serializers import PollSerializer, PollVoteSerializer


class PollListCreate(APIView):
    """
    GET  /api/polls/         -> paginated list of polls (+ options)
    POST /api/polls/         -> create poll with nested options
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        queryset = (
                Poll.objects.all()
                .prefetch_related(Prefetch("options", queryset=PollOption.objects.order_by("id")))
        )

        paginator = LimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = PollSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = PollSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        poll = serializer.save()  # creates Poll and its PollOption rows
        return Response(PollSerializer(poll, context={"request": request}).data,
                        status=status.HTTP_201_CREATED)

class PollDetail(APIView):
    """
    GET    /api/polls/<id>/  -> retrieve poll
    PATCH  /api/polls/<id>/  -> upsert options; nothing deleted
    PUT    /api/polls/<id>/  -> replace; missing options are deleted
    DELETE /api/polls/<id>/  -> delete poll (and its options/votes via FK)
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk: int) -> Poll:
        try:
            return (
                Poll.objects
                .prefetch_related(Prefetch("options", queryset=PollOption.objects.order_by("id")))
                .get(pk=pk)
            )
        except Poll.DoesNotExist:
            raise Http404

    def get(self, request, pk: int):
        poll = self.get_object(pk)
        serializer = PollSerializer(poll, context={"request": request})
        return Response(serializer.data)

    def patch(self, request, pk: int):
        poll = self.get_object(pk)
        serializer = PollSerializer(
            poll, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        poll = serializer.save()
        return Response(PollSerializer(poll, context={"request": request}).data)

    def put(self, request, pk: int):
        poll = self.get_object(pk)
        serializer = PollSerializer(
            poll, data=request.data, partial=False, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        poll = serializer.save()
        return Response(PollSerializer(poll, context={"request": request}).data)

    def delete(self, request, pk: int):
        poll = self.get_object(pk)
        poll.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PollVoteCreate(APIView):
    """
    POST /api/poll-votes/ -> create a vote
       Body: {"poll": <poll_id>, "option": <option_id>}
       - user is taken from request.user
       - validates poll window, is_active, max_votes/user, and option-in-poll
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PollVoteSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        vote = serializer.save()
        return Response(PollVoteSerializer(vote, context={"request": request}).data,
                        status=status.HTTP_201_CREATED)
