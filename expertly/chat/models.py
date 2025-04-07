from django.db import models
from accounts.models import User

class ChatRoom(models.Model):
    participant1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatrooms_as_p1')
    participant2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatrooms_as_p2')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('participant1', 'participant2')
    
    def __str__(self):
        return f"Chat between {self.participant1.username} and {self.participant2.username}"

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message from {self.sender.username} in {self.chat_room}"