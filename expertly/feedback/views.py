from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from django.db import models
from .models import Feedback
from .serializers import FeedbackSerializer, CreateFeedbackSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateFeedbackSerializer
        return FeedbackSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        if hasattr(user, 'expert'):
            return queryset.filter(appointment__expert=user.expert)
        elif hasattr(user, 'client_profile'):
            return queryset.filter(client=user.client_profile)
        return queryset.none()

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'client_profile'):
            raise serializers.ValidationError(
                {"error": "Only clients can create feedback"},
                code=status.HTTP_403_FORBIDDEN
            )
            
        appointment = serializer.validated_data.get('appointment')
        if not appointment or not hasattr(appointment, 'expert'):
            raise serializers.ValidationError(
                {"error": "Valid appointment with expert is required"},
                code=status.HTTP_400_BAD_REQUEST
            )
            
        serializer.save(
            client=user.client_profile,
            expert=appointment.expert
        )