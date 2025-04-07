from django.db import models

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    # String reference to Appointment
    appointment = models.OneToOneField(
    'appointment.Appointment',
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    related_name='payment_record'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='ETB')
    tx_ref = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    chapa_transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_paid(self):
        return self.status == 'completed'

    def __str__(self):
        return f"Payment #{self.id} - {self.amount} {self.currency} ({self.status})"