#BragiApp\chat\consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatThread, Message
import base64
from django.core.files.base import ContentFile
from io import BytesIO

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
        event_type = text_data_json.get("type")

        if event_type == "typing":
            await self.channel_layer.group_send(
                self.thread_group_name,
                {
                    "type": "chat.typing",
                    "sender": self.scope['user'].username
                }
            )
        elif event_type == "stop_typing":
            await self.channel_layer.group_send(
                self.thread_group_name,
                {
                    "type": "chat.stop_typing",
                    "sender": self.scope['user'].username
                }
            )
        elif event_type == "message":
            message = text_data_json.get("message", "").strip()
            file_data = text_data_json.get("file")  # Expecting base64 encoded file
            if not message and not file_data:
                return

            user = self.scope['user']
            thread_id = self.thread_name
            try:
                thread = await database_sync_to_async(ChatThread.objects.get)(id=thread_id)
            except ChatThread.DoesNotExist:
                await self.close()
                return

            # Save message and optionally a file
            message_obj = await database_sync_to_async(Message.objects.create)(
                thread=thread,
                sender=user,
                content=message
            )

            if file_data:
                file_name = f"file_{message_obj.id}.txt"  # You can adjust the file name and type
                decoded_file = base64.b64decode(file_data)
                file = ContentFile(decoded_file, name=file_name)
                message_obj.file = file
                await database_sync_to_async(message_obj.save)()

            file_url = message_obj.file.url if message_obj.file else None

            # Send message to the thread group
            await self.channel_layer.group_send(
                self.thread_group_name,
                {
                    "type": "chat.message",
                    "message": message,
                    "file": file_url,
                    "sender": user.username,
                    "sender_profile_picture": await database_sync_to_async(self.get_profile_picture_url)(user),
                    "timestamp": message_obj.timestamp.strftime("%H:%M")
                }
            )

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        sender_profile_picture = event["sender_profile_picture"]
        timestamp = event["timestamp"]
        file = event.get("file")

        await self.send(
            text_data=json.dumps(
                {
                    "type": "message",
                    "message": message,
                    "file": file,
                    "sender": sender,
                    "sender_profile_picture": sender_profile_picture,
                    "timestamp": timestamp,
                }
            )
        )

    async def chat_typing(self, event):
        sender = event["sender"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "typing",
                    "sender": sender,
                }
            )
        )

    async def chat_stop_typing(self, event):
        sender = event["sender"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "stop_typing",
                    "sender": sender,
                }
            )
        )

    def get_profile_picture_url(self, user):
        """Helper method to get the profile picture URL synchronously"""
        return user.userprofile.profile_picture.url if user.userprofile.profile_picture else "/static/img/default_profile_picture.png"
