from rest_framework import serializers
from .models import Notification
from appointment.serializers import AppointmentSerializer

class NotificationSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'appointment', 'title', 'message',
            'notification_type', 'is_read', 'created_at'
        ]
        read_only_fields = ['created_at']