from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Notification
from django.utils import timezone
from django.db.models import Q
from accounts.models import User
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_email_notification(self, notification_id):
    """
    Send email notification with retry logic
    Args:
        notification_id: ID of the Notification record
    """
    try:
        notification = Notification.objects.get(id=notification_id)
        user = notification.user
        
        context = {
            'title': notification.title,
            'message': notification.message,
            'notification_type': notification.notification_type,
            'user': user.get_full_name()
        }

        # Render HTML and text versions
        html_message = render_to_string('notification/email_template.html', context)
        plain_message = render_to_string('notification/email_template.txt', context)

        send_mail(
            subject=notification.title,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False
        )
        
        logger.info(f"Sent email notification #{notification_id} to {user.email}")
        return True

    except Notification.DoesNotExist:
        logger.error(f"Notification #{notification_id} not found")
        raise
    except Exception as e:
        logger.error(f"Failed to send notification #{notification_id}: {str(e)}")
        raise self.retry(exc=e)

@shared_task
def process_notification_delivery(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        
        # Email delivery
        if notification.user.email_notifications_enabled:
            send_email_notification.delay(notification_id)    
        return f"Processed notification #{notification_id}"
    
    except Exception as e:
        logger.error(f"Notification processing failed: {str(e)}")
        raise

@shared_task
def bulk_notification_cleanup(days_old=30):

    cutoff_date = timezone.now() - timezone.timedelta(days=days_old)
    deleted_count, _ = Notification.objects.filter(
        Q(created_at__lt=cutoff_date) & 
        Q(is_read=True)
    ).delete()
    
    logger.info(f"Deleted {deleted_count} old notifications")
    return deleted_count