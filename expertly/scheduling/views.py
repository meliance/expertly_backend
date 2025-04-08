from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Schedule, TimeOff
from .serializers import (
    ScheduleSerializer, CreateScheduleSerializer,
    TimeOffSerializer, CreateTimeOffSerializer
)

class ScheduleListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'expert':
            return Schedule.objects.filter(expert=self.request.user.expert_profile)
        return Schedule.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateScheduleSerializer
        return ScheduleSerializer
    
    def perform_create(self, serializer):
        if self.request.user.user_type == 'expert':
            serializer.save(expert=self.request.user.expert_profile)
        else:
            raise permissions.PermissionDenied("Only experts can create schedules")

class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'expert':
            return Schedule.objects.filter(expert=self.request.user.expert_profile)
        return Schedule.objects.none()

class ExpertScheduleListView(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        expert_id = self.kwargs['expert_id']
        return Schedule.objects.filter(expert_id=expert_id, is_available=True)

class TimeOffListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'expert':
            return TimeOff.objects.filter(expert=self.request.user.expert_profile)
        return TimeOff.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTimeOffSerializer
        return TimeOffSerializer
    
    def perform_create(self, serializer):
        if self.request.user.user_type == 'expert':
            serializer.save(expert=self.request.user.expert_profile)
        else:
            raise permissions.PermissionDenied("Only experts can create time offs")

class TimeOffDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TimeOffSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'expert':
            return TimeOff.objects.filter(expert=self.request.user.expert_profile)
        return TimeOff.objects.none()