# appointments/models.py
from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import Client, Expert
from scheduling.models import Schedule

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('payment_pending', 'Payment Pending'),
    )
    
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='client_appointments'
    )
    expert = models.ForeignKey(
        Expert,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.PROTECT,
        related_name='appointments'
    )
    payment = models.OneToOneField(
        'payments.Payment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointment_link'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    description = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = [
            ('client', 'schedule'),
            ('expert', 'schedule')
        ]

    def __str__(self):
        expert_name = self.expert.user.username if self.expert else "No Expert"
        return f"Appointment #{self.id} - {self.client.user.username} with {expert_name}"

    def clean(self):
        """Validate appointment constraints"""
        if self.status == 'confirmed' and not self.payment:
            raise ValidationError("You must complete the payment")
        
        if self.status == 'completed' and not self.has_paid:
            raise ValidationError("Cannot complete unpaid appointments")

    @property
    def has_paid(self):
        """Safely check payment status without direct import"""
        return hasattr(self, 'payment') and self.payment and self.payment.status == 'completed'

    def save(self, *args, **kwargs):
        """Handle status transitions"""
        self.full_clean()
        
        if self.has_paid and self.status == 'pending':
            self.status = 'confirmed'
            
        super().save(*args, **kwargs)