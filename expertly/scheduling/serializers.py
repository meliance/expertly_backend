from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'expert_id', 'start_time', 'end_time', 'duration', 'daily_availability']