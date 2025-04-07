from rest_framework import serializers
from .models import Payment
from appointment.serializers import AppointmentSerializer

class PaymentSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('status', 'chapa_transaction_id', 'created_at', 'updated_at')

class InitiatePaymentSerializer(serializers.Serializer):
    appointment_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(default='ETB')