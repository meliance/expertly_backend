from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from feedback.models import Feedback

@receiver(post_save, sender=Feedback)
def create_feedback_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.expert.user,
            appointment=instance.appointment,
            title=f"New Feedback from {instance.client.user.username}",
            message=f"You received {instance.rating} stars rating",
            notification_type='feedback'
        )
from notification.tasks import process_notification_delivery

@receiver(post_save, sender=Notification)
def trigger_notification_delivery(sender, instance, created, **kwargs):
    """Automatically process delivery for new notifications"""
    if created:
        process_notification_delivery.delay(instance.id)