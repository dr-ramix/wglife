from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.db import transaction
from .models import DayOff
from .serializers import DayOffSerializer


class DayOffs(APIView):

    def get(self, request):
        dayoffs = DayOff.objects.all()

        user_id = request.query_params.get("userid")
        date = request.query_params.get("date")
        start_date = request.query_params.get("date-start")
        end_date = request.query_params.get("date-end")
        mode = request.query_params.get("mode")

        if user_id:
            dayoffs = dayoffs.filter(user=user_id)
        if date:
            parsed_date = parse_date(date)
            if parsed_date:
                dayoffs = dayoffs.filter(date=parsed_date)
        if start_date:
            parsed_start = parse_date(start_date)
            if parsed_start:
                dayoffs = dayoffs.filter(date__gte=parsed_start)
        if end_date:
            parsed_end = parse_date(end_date)
            if parsed_end:
                dayoffs = dayoffs.filter(date__lte=parsed_end)
        if mode:
            dayoffs = dayoffs.filter(mode=mode)

        serializers = DayOffSerializer(dayoffs, many=True)

        return Response(serializers.date, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DayOffSerializer(data=datarequest)
        try:
            if serializer.is_valid(raise_exception=False):
                with transaction.atomic():
                    serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # Validation errors → 400
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except DatabaseError as db_err:
            # DB-level issue (e.g., constraint fail, deadlock, etc.)
            return Response(
                {"detail": f"Database error: {str(db_err)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as exc:
            # Catch-all for unexpected errors
            return Response(
                {"detail": f"Unexpected error: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




