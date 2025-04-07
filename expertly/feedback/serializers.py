# feedback/serializers.py
from rest_framework import serializers
from .models import Feedback
from accounts.serializers import ClientSerializer, ExpertSerializer
from appointment.serializers import AppointmentSerializer

class FeedbackSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    expert = ExpertSerializer(read_only=True)
    appointment = AppointmentSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class CreateFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('appointment', 'rating', 'review')

    def validate(self, data):
        appointment = data['appointment']
        request = self.context.get('request')

        if appointment.client != request.user.client:
            raise serializers.ValidationError("You can only leave feedback for your own appointments")
            
        if appointment.status != 'completed':
            raise serializers.ValidationError("You can only leave feedback for completed appointments")
            
        if Feedback.objects.filter(appointment=appointment).exists():
            raise serializers.ValidationError("Feedback already exists for this appointment")
            
        return data