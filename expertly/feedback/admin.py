from django.contrib import admin
from .models import Feedback, Expert

@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'expert', 'appointment', 'rating', 'review')
    search_fields = ('client__name', 'expert__name', 'appointment__id')