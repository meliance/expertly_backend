from django.db.models.signals import post_save
from django.dispatch import receiver
from payments.models import Payment

@receiver(post_save, sender=Payment)
def update_appointment_status(sender, instance, created, **kwargs):
    if hasattr(instance, 'appointment_link'):
        appointment = instance.appointment_link
        
        if instance.status == 'completed':
            if appointment.status in ['pending', 'payment_pending']:
                appointment.status = 'confirmed'
                appointment.save()
        elif instance.status == 'failed':
            appointment.status = 'payment_pending'
            appointment.save()