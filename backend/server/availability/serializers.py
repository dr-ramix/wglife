from rest_framework import serializers


class DayOff(serializers.ModelSerializer):
    class Meta:
        model = DayOff
        field = ["__all__"]