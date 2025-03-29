from django.contrib import admin
from .models import Expert, Schedule, Client, Appointment

@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'expert', 'start_time', 'end_time', 'duration', 'daily_availability')
    search_fields = ('expert__name',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'schedule', 'status', 'description')
    search_fields = ('client__name', 'schedule__expert__name')