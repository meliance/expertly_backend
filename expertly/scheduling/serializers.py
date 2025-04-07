from rest_framework import serializers
from .models import Schedule, TimeOff
from accounts.serializers import ExpertSerializer

class ScheduleSerializer(serializers.ModelSerializer):
    expert = ExpertSerializer(read_only=True)
    
    class Meta:
        model = Schedule
        fields = '__all__'

class CreateScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['day_of_week', 'start_time', 'end_time', 'duration', 'is_available']
    
    def validate(self, attrs):
        # Add validation logic here (e.g., check for overlapping schedules)
        return attrs

class TimeOffSerializer(serializers.ModelSerializer):
    expert = ExpertSerializer(read_only=True)
    
    class Meta:
        model = TimeOff
        fields = '__all__'

class CreateTimeOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeOff
        fields = ['start_datetime', 'end_datetime', 'reason']
    
    def validate(self, attrs):
        # Add validation logic here (e.g., check for overlapping time offs)
        return attrs