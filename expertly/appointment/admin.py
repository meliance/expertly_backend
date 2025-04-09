from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('expert', 'client', 'status', 'schedule', 'created_at')  # Removed payment
    raw_id_fields = ('client', 'expert', 'schedule')  # Removed payment
    list_filter = ('status', 'created_at')
    search_fields = ('client__username', 'expert__user__username')