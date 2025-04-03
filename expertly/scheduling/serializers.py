from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z")
    end_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z")

    class Meta:
        model = Schedule
        fields = "__all__"
