from django.contrib import admin
from .models import ChatRoom, Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant1', 'participant2', 'created_at', 'updated_at')
    list_display_links = ('id',)
    list_filter = ('created_at', 'updated_at')
    search_fields = (
        'participant1__username', 
        'participant1__email',
        'participant2__username',
        'participant2__email'
    )
    raw_id_fields = ('participant1', 'participant2')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('participant1', 'participant2')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_room', 'sender', 'truncated_content', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp', 'chat_room')
    search_fields = (
        'sender__username',
        'sender__email',
        'content',
        'chat_room__participant1__username',
        'chat_room__participant2__username'
    )
    raw_id_fields = ('sender', 'chat_room')
    readonly_fields = ('timestamp',)
    list_editable = ('is_read',)
    list_per_page = 30

    def truncated_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    truncated_content.short_description = 'Content'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('sender', 'chat_room')