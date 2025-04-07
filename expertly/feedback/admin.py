from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'expert', 'appointment', 'rating', 'review')
    search_fields = ('client__name', 'expert__name', 'appointment__id')