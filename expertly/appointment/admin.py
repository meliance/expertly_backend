# appointments/admin.py
from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_info', 'expert_info', 'schedule', 'status', 'has_paid', 'created_at')
    list_filter = ('status', 'expert', 'created_at')
    search_fields = ('client__user__username', 'expert__user__username', 'description')
    raw_id_fields = ('client', 'expert', 'schedule', 'payment')
    date_hierarchy = 'created_at'

    def client_info(self, obj):
        return obj.client.user.username
    client_info.short_description = 'Client'

    def expert_info(self, obj):
        return obj.expert.user.username if obj.expert else "None"
    expert_info.short_description = 'Expert'

    def has_paid(self, obj):
        return obj.has_paid
    has_paid.boolean = True
    has_paid.short_description = 'Paid'