# appointments/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Appointment
from .serializers import AppointmentSerializer, CreateAppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateAppointmentSerializer
        return AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'client'):
            return self.queryset.filter(client=user.client)
        elif hasattr(user, 'expert'):
            return self.queryset.filter(expert=user.expert)
        return self.queryset.none()

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'client'):
            appointment = serializer.save(client=self.request.user.client)
            
            # Set status to payment_pending if expert requires payment
            if appointment.expert and appointment.expert.requires_payment:
                appointment.status = 'payment_pending'
                appointment.save()
        else:
            raise PermissionDenied("Only clients can create appointments.")