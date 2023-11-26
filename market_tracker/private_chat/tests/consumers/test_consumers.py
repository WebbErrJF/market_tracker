import datetime
from django.contrib.auth.models import User
from unittest.mock import patch
import json
from django.test import TestCase
from private_chat.consumers import ChatConsumer
from unittest.mock import AsyncMock


class TestChatConsumer(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test_user', password='testpassword')

    @patch('private_chat.consumers.ChatConsumer._handel_message')
    @patch('private_chat.consumers.ChatConsumer._send_chat_history')
    async def test_receive(self, send_chat_history, handel_message):
        consumer = ChatConsumer()
        data_message = {'type': 'message', 'message': 'Test message'}
        consumer.scope = {'user': 'test_user'}
        await consumer.receive(json.dumps(data_message))
        handel_message.assert_called_once()
        handel_message.assert_called_with(data_message)

    @patch('private_chat.consumers.datetime')
    @patch('private_chat.consumers.ChatConsumer._save_msg_to_database')
    @patch('private_chat.consumers.ChatConsumer._send_chat_message')
    async def test_handel_message(self, send_chat_message, save_msg_to_database, datetime_obj):
        expected_datetime = datetime.datetime(2023, 11, 12, 12, 0, 0)
        datetime_obj.now.return_value = expected_datetime
        expected_user = 'test_user'
        expected_message = 'Test message'
        consumer = ChatConsumer()
        data_message = {'type': 'message', 'message': 'Test message'}
        consumer.scope = {'user': 'test_user'}
        await consumer._handel_message(data_message)
        send_chat_message.assert_called_once()
        send_chat_message.assert_called_with(expected_message, expected_user, expected_datetime)
        save_msg_to_database.assert_called_once()
        save_msg_to_database.assert_called_with(expected_message, expected_user, expected_datetime)

    async def test_send_chat_message(self):
        consumer = ChatConsumer()
        consumer.scope = {'user': 'test_user'}
        consumer.room_group_name = 'test_group_name'
        consumer.channel_layer = AsyncMock()

        date = datetime.datetime.now()
        expected_date_string = date.strftime('%I:%M %p, %d-%m-%Y')
        expected_argument = {"type": "chat.message",
                             "message": 'test',
                             "senderUsername": 'test_user',
                             "formatted_time_stamp": expected_date_string,
                             "logged_user": consumer.logged_user
                             }
        await consumer._send_chat_message('test', 'test_user', date)
        consumer.channel_layer.group_send.assert_called_once()
        consumer.channel_layer.group_send.assert_called_with(consumer.room_group_name, expected_argument)

    @patch('private_chat.consumers.json.dumps')
    @patch('private_chat.consumers.ChatConsumer.get_messages')
    async def test__send_chat_history(self, get_messages, dumps):
        dumps.side_effect = lambda x: x
        get_messages.return_value = 'test msg'
        consumer = ChatConsumer()
        consumer.scope = {"user": self.test_user}
        expected_argument = {
            "type": "chat.history",
            "messages": 'test msg',
            "logged_user": "test_user"}
        consumer.send = AsyncMock()
        await consumer._send_chat_history()
        consumer.send.assert_called_once()
        consumer.send.assert_called_with(text_data=expected_argument)

    def test_generate_room_name(self):
        consumer = ChatConsumer()
        test_user_2 = User.objects.create(username='test_user_2', password='testpassword')
        consumer.scope = {"user": self.test_user}
        expected_room_name = f"chat_{test_user_2.id}_{self.test_user.id}"
        self.assertEqual(
            consumer._generate_room_name(test_user_2.id),
            expected_room_name
        )