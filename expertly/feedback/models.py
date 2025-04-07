from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import Client, Expert
from appointment.models import Appointment

class Feedback(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='given_feedbacks')
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='received_feedbacks')
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='feedback'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('client', 'appointment')
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback #{self.id} ({self.rating} stars)"