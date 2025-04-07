# appointments/serializers.py
from rest_framework import serializers
from .models import Appointment
from accounts.serializers import ClientSerializer, ExpertSerializer
from scheduling.serializers import ScheduleSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    expert = ExpertSerializer(read_only=True, allow_null=True)
    schedule = ScheduleSerializer(read_only=True)
    has_paid = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('status', 'created_at', 'updated_at')

class CreateAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('expert', 'schedule', 'description')

    def validate(self, data):
        # Add custom validation logic here
        schedule = data.get('schedule')
        expert = data.get('expert')
        
        if expert and schedule.expert != expert:
            raise serializers.ValidationError("Schedule doesn't belong to this expert")
        
        return data