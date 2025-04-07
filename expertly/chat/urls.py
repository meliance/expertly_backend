from django.urls import path
from .views import (
    ChatRoomListView, ChatRoomDetailView,
    MessageListView, MarkMessagesAsReadView,
    GetOrCreateChatRoomView
)

urlpatterns = [
    path('chatrooms/', ChatRoomListView.as_view(), name='chatroom-list'),
    path('chatrooms/<int:pk>/', ChatRoomDetailView.as_view(), name='chatroom-detail'),
    path('chatrooms/<int:chat_room_id>/messages/', MessageListView.as_view(), name='message-list'),
    path('chatrooms/<int:chat_room_id>/mark-read/', MarkMessagesAsReadView.as_view(), name='mark-messages-read'),
    path('chatrooms/get-or-create/', GetOrCreateChatRoomView.as_view(), name='get-or-create-chatroom'),
]