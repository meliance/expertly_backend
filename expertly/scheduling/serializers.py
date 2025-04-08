from rest_framework import serializers
from .models import Schedule, TimeOff
from accounts.serializers import ExpertSerializer

class ScheduleSerializer(serializers.ModelSerializer):
    expert = ExpertSerializer(read_only=True)
<<<<<<< Updated upstream
    
    class Meta:
        model = Schedule
        fields = '__all__'
=======

    class Meta:
        model = Schedule
        fields = '__all__'  # Use '__all__' to include all model fields
>>>>>>> Stashed changes

class CreateScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
<<<<<<< Updated upstream
        fields = ['day_of_week', 'start_time', 'end_time', 'duration', 'is_available']
    
    def validate(self, attrs):
        # Add validation logic here (e.g., check for overlapping schedules)
=======
        fields = ['expert', 'day_of_week', 'start_time', 'end_time', 'duration', 'is_available']
    
    def validate(self, attrs):
        # Check for overlapping schedules
>>>>>>> Stashed changes
        return attrs

class TimeOffSerializer(serializers.ModelSerializer):
    expert = ExpertSerializer(read_only=True)
<<<<<<< Updated upstream
    
    class Meta:
        model = TimeOff
        fields = '__all__'
=======

    class Meta:
        model = TimeOff
        fields = '__all__'  # Use '__all__' to include all model fields
>>>>>>> Stashed changes

class CreateTimeOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeOff
<<<<<<< Updated upstream
        fields = ['start_datetime', 'end_datetime', 'reason']
    
    def validate(self, attrs):
        # Add validation logic here (e.g., check for overlapping time offs)
=======
        fields = ['expert', 'start_datetime', 'end_datetime', 'reason']
    
    def validate(self, attrs):
        # Check for overlapping time offs
>>>>>>> Stashed changes
        return attrs