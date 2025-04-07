from django.contrib import admin
from .models import Schedule, TimeOff

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    # Your schedule admin configuration
    pass

@admin.register(TimeOff)
class TimeOffAdmin(admin.ModelAdmin):
    # Your time off admin configuration
    pass