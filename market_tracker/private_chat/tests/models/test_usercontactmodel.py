from django.test import TestCase
from private_chat.models import UserContact
from django.contrib.auth.models import User


class UserContactModelTest(TestCase):
    def setUp(self):
        test_user = User.objects.create(username='testuser',
                                        password='testpassword')
        test_contact_user = User.objects.create(username='testcontact',
                                                password='testpassword')

        self.test_user_contact = UserContact.objects.create(user=test_user,
                                                            contact=test_contact_user)

    def test_if_test_user_contact_is_instance_of_UserContact(self):
        self.assertTrue(isinstance(self.test_user_contact, UserContact))
