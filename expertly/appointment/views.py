# appointment/views.py
from rest_framework import viewsets
from .models import Appointment
from .serializers import AppointmentSerializer
from rest_framework.permissions import IsAuthenticated

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        
        if hasattr(user, 'client_profile'):
            return qs.filter(client=user.client_profile)
        elif hasattr(user, 'expert'):
            return qs.filter(expert=user.expert)
        
        return qs.none()