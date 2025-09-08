from rest_framework import serializers


class DayOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayOff
        field = ["__all__"]