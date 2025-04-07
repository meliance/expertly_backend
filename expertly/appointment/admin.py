# appointment/admin.py
from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'expert', 'status', 'schedule')
    list_filter = ('status', 'created_at')
    search_fields = ('client__user__username', 'expert__user__username')
    raw_id_fields = ('client', 'expert', 'schedule', 'payment')