from django.contrib import admin
from .models import Schedule, TimeOff

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('expert', 'day_of_week', 'start_time', 'end_time', 'is_available')
    search_fields = ('expert__user__username',)  # Search by expert's username
    list_filter = ('day_of_week', 'is_available')

@admin.register(TimeOff)
class TimeOffAdmin(admin.ModelAdmin):
    list_display = ('expert', 'start_datetime', 'end_datetime', 'reason')
    search_fields = ('expert__user__username',)
    list_filter = ('start_datetime',)