# BragiApp\chat\consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

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

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to thread group
        await self.channel_layer.group_send(
            self.thread_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from thread group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
