from django.db import models
from django.conf import settings
from appointment.models import Appointment

class Chat(models.Model):
    appointment = models.ForeignKey(Appointment, null=True, on_delete=models.CASCADE)  # Allow null values
    sender = models.CharField(max_length=255, default="system_user")
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat message from {self.sender} for appointment {self.appointment.id if self.appointment else 'N/A'}"