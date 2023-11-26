from django.test import TestCase
from django.urls import reverse_lazy
from users.tests.views.client import test_client
from django.contrib.auth.models import User


class TestDisplayProfileView(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test_user', password='testpassword')

    def test_should_return_status_code_200(self):
        url = reverse_lazy('display_profile', kwargs={'user_id': self.test_user.id})
        expected_status_code = 200
        resp = test_client.get(url)
        actual_status_code = resp.status_code

        self.assertEquals(expected_status_code, actual_status_code)

    def test_should_return_valid_template(self):
        url = reverse_lazy('display_profile', kwargs={'user_id': self.test_user.id})
        expected_template_path = "users/display_profile.html"
        resp = test_client.get(url)
        actual_template_path = resp.templates[0].name

        self.assertEqual(actual_template_path, expected_template_path)

    def test_should_return_valid_context(self):
        url = reverse_lazy('display_profile', kwargs={'user_id': self.test_user.id})
        expected_context = {'username': self.test_user.username,
                            'profile_description': self.test_user.profile.description,
                            'user_id': self.test_user.id,
                            'profile_img': self.test_user.profile.image.url}
        resp = test_client.get(url)

        self.assertEqual(resp.context['username'], expected_context['username'])
        self.assertEqual(resp.context['profile_description'], expected_context['profile_description'])
        self.assertEqual(resp.context['user_id'], expected_context['user_id'])
        self.assertEqual(resp.context['profile_img'], expected_context['profile_img'])
