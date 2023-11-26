import json
from .models import Message
from django.contrib.auth import get_user_model
from .serializers import MessageSerializer
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None
        self.logged_user = None
        self.decision_receive_dict = {'message': self._handel_message,
                                      'change_contact': self._change_contact}

    async def connect(self):
        self.room_group_name = self._generate_room_name(self.scope['url_route']['kwargs']['other_user_id'])
        self.logged_user = self.scope['url_route']['kwargs']['user']
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self._send_chat_history()

    async def _send_chat_history(self):
        messages = await self.get_messages()
        await self.send(text_data=json.dumps(
            {"type": "chat.history",
             "messages": messages,
             "logged_user": self.scope['user'].username
             }))

    def _generate_room_name(self, other_user_id):
        self_user_id = self.scope['user'].id
        room_name = (
            f'{self_user_id}_{other_user_id}'
            if int(self_user_id) > int(other_user_id)
            else f'{other_user_id}_{self_user_id}'
        )
        return f"chat_{room_name}"

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        await self.decision_receive_dict[text_data_json['type']](text_data_json)

    async def _change_contact(self, data):
        other_user_id = data["change_contact"]
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        self.room_group_name = self._generate_room_name(other_user_id)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self._send_chat_history()

    async def _handel_message(self, data):
        sender_username = str(self.scope['user'])
        message = data["message"]
        date = datetime.now()
        await self._save_msg_to_database(message, sender_username, date)
        await self._send_chat_message(message, sender_username, date)

    async def _send_chat_message(self, message, sender_username, date):
        date_to_display = date.strftime('%I:%M %p, %d-%m-%Y')
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message",
             "message": message,
             "senderUsername": sender_username,
             "formatted_time_stamp": date_to_display,
             "logged_user": self.logged_user
             }
        )

    async def _save_msg_to_database(self, message, sender_username, date):
        sender = await self.get_user(sender_username.replace('"', ''))
        await self.save_message(sender=sender, message=message, thread_name=self.room_group_name, date=date)

    async def get_user(self, username):
        return await get_user_model().objects.filter(username=username).afirst()

    async def get_messages(self):
        messages = Message.objects.select_related().filter(thread_name=self.room_group_name).all()
        serialized_messages = [MessageSerializer(message).data async for message in messages]
        return serialized_messages

    async def save_message(self, sender, message, thread_name, date):
        await Message.objects.acreate(sender=sender, message=message, thread_name=thread_name, time_stamp=date)

    async def chat_message(self, event):
        message = event["message"]
        username = event['senderUsername']
        formatted_time_stamp = event['formatted_time_stamp']
        message_to_send = {
            "message": message,
            'username': username,
            'logged_user': self.logged_user,
            'formatted_time_stamp': formatted_time_stamp
        }
        await self.send(text_data=json.dumps(message_to_send))
