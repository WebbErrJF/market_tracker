from django.test import TestCase
from private_chat.models import Message, UserContact
from datetime import datetime
from django.contrib.auth.models import User


class MyModelTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create(username='testuser',
                                        password='testpassword')
        self.test_timestamp = datetime.now()
        self.test_message = Message.objects.create(sender=test_user,
                                                   message='test message',
                                                   thread_name='test thread',
                                                   time_stamp=self.test_timestamp)

    def test_message_sender(self):
        self.assertEqual(self.test_message.sender.username, 'testuser')

    def test_message_message(self):
        self.assertEqual(self.test_message.message, 'test message')

    def test_message_thread_name(self):
        self.assertEqual(self.test_message.thread_name, 'test thread')

    def test_message_time_stamp(self):
        self.assertEqual(self.test_message.time_stamp, self.test_timestamp)
