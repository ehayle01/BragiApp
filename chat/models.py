# BragiApp/chat/models.py
from django.contrib.auth.models import User
from django.db import models


class ChatThread(models.Model):
    user1 = models.ForeignKey(User, related_name='thread_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='thread_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}"


class Message(models.Model):
    thread = models.ForeignKey(ChatThread, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    file = models.FileField(upload_to="chat_files/", null=True, blank=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"