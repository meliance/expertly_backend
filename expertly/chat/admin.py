from django.contrib import admin
from .models import Chat

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment', 'sender', 'message', 'timestamp')  # Ensure these fields exist in Chat
    search_fields = ('appointment__id', 'sender__username', 'message')  # Adjust as per your User model