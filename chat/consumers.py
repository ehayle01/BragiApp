# BragiApp/chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatThread, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_name = self.scope["url_route"]["kwargs"]["thread_name"]
        self.thread_group_name = f"chat_{self.thread_name}"

        # Join thread group
        await self.channel_layer.group_add(self.thread_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave thread group
        await self.channel_layer.group_discard(self.thread_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message", "").strip()

        # Ensure non-empty message
        if not message:
            return

        # Get sender (user)
        user = self.scope['user']
        if not user.is_authenticated:
            return

        # Save message to database
        thread_id = self.thread_name  # Assuming thread_name is the thread ID
        try:
            thread = await database_sync_to_async(ChatThread.objects.get)(id=thread_id)
        except ChatThread.DoesNotExist:
            await self.close()
            return

        await database_sync_to_async(Message.objects.create)(
            thread=thread,
            sender=user,
            content=message
        )

        # Send message to thread group
        await self.channel_layer.group_send(
            self.thread_group_name, {"type": "chat.message", "message": message, "sender": user.username}
        )

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender": sender}))
