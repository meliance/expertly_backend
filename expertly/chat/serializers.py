from rest_framework import serializers
from .models import ChatRoom, Message
from accounts.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'chat_room', 'sender', 'content', 'timestamp', 'is_read']
        read_only_fields = ['timestamp', 'is_read']

class ChatRoomSerializer(serializers.ModelSerializer):
    participant1 = UserSerializer(read_only=True)
    participant2 = UserSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'participant1', 'participant2', 'created_at', 'updated_at', 'last_message', 'unread_count']
    
    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0

class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content']
    
    def create(self, validated_data):
        chat_room = self.context.get('chat_room')
        sender = self.context.get('sender')
        
        if not chat_room or not sender:
            raise serializers.ValidationError("Missing required context")
        
        if sender not in [chat_room.participant1, chat_room.participant2]:
            raise serializers.ValidationError("You are not a participant in this chat room")
        
        message = Message.objects.create(
            chat_room=chat_room,
            sender=sender,
            content=validated_data['content'],
            is_read=False
        )
        return message