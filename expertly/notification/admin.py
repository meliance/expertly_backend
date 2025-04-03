from django.contrib import admin
from .models import Notification, Appointment

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment', 'title', 'message', 'notification_type', 'created_at')
    search_fields = ('appointment__id', 'title', 'message')