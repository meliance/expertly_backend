from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import models
from .models import ChatRoom, Message
from .serializers import (
    ChatRoomSerializer, MessageSerializer,
    CreateMessageSerializer
)
from accounts.models import User

class ChatRoomListView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(
            models.Q(participant1=user) | models.Q(participant2=user)
        ).distinct().prefetch_related('participant1', 'participant2', 'messages')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ChatRoomDetailView(generics.RetrieveAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'  
    lookup_url_kwarg = None  # This tells DRF to use the same name as lookup_field
    
    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(
            models.Q(participant1=user) | models.Q(participant2=user)
        ).prefetch_related('participant1', 'participant2', 'messages')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
class MessageListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        chat_room_id = self.kwargs['chat_room_id']
        return Message.objects.filter(chat_room_id=chat_room_id).order_by('timestamp')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateMessageSerializer
        return MessageSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['chat_room'] = ChatRoom.objects.get(id=self.kwargs['chat_room_id'])
        context['sender'] = self.request.user
        return context
    
    def perform_create(self, serializer):
        # The actual creation is now handled by the serializer with context
        serializer.save()

class MarkMessagesAsReadView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        chat_room_id = kwargs['chat_room_id']
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        
        if request.user not in [chat_room.participant1, chat_room.participant2]:
            raise permissions.PermissionDenied("You are not a participant in this chat room")
        
        updated_count = Message.objects.filter(
            chat_room=chat_room,
            is_read=False
        ).exclude(
            sender=request.user
        ).update(is_read=True)
        
        return Response(
            {'status': f'{updated_count} messages marked as read'}, 
            status=status.HTTP_200_OK
        )

class GetOrCreateChatRoomView(generics.GenericAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        participant_id = request.data.get('participant_id')
        
        if not participant_id:
            return Response(
                {'error': 'participant_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            participant = User.objects.get(id=participant_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Participant not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if participant == request.user:
            return Response(
                {'error': 'Cannot create chat room with yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check existing chat room (both directions)
        chat_room = ChatRoom.objects.filter(
            models.Q(participant1=request.user, participant2=participant) |
            models.Q(participant1=participant, participant2=request.user)
        ).first()
        
        if not chat_room:
            chat_room = ChatRoom.objects.create(
                participant1=request.user,
                participant2=participant
            )
        
        serializer = self.get_serializer(chat_room, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)