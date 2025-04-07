from django.db import models
from appointment.models import Appointment
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('feedback', 'Feedback'),
        ('appointment', 'Appointment'),
        ('system', 'System'),
        ('payment', 'Payment'),
    )
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    appointment = models.ForeignKey(
        Appointment, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPES
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]

    def __str__(self):
        return f"{self.notification_type} notification for {self.user.username}"

    @classmethod
    def create_appointment_notification(cls, appointment, title, message):
        """
        Creates notifications for both client and expert in an appointment
        """
        notifications = []
        
        # Ensure the client has a user
        if appointment.client and appointment.client.user:
            notifications.append(cls(
                user=appointment.client.user,
                appointment=appointment,
                title=title,
                message=message,
                notification_type='appointment'
            ))
        else:
            print("Client does not have a valid user.")
        
        # Ensure the expert has a user
        if appointment.expert and appointment.expert.user:
            notifications.append(cls(
                user=appointment.expert.user,
                appointment=appointment,
                title=title,
                message=message,
                notification_type='appointment'
            ))
        else:
            print("Expert does not have a valid user.")
        
        return cls.objects.bulk_create(notifications)
