from django.test import TestCase
from django.urls import reverse_lazy
from private_chat.tests.views.client import test_client
from django.contrib.auth.models import User


class TestHomepageView(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_should_redirect_if_not_logged_in(self):
        response = test_client.get(reverse_lazy('chat'))
        self.assertRedirects(response, '/login/?next=%2Fchat%2F')

    def test_logged_in_uses_correct_template(self):
        login = test_client.login(username='testuser', password='testpassword')
        response = test_client.get(reverse_lazy('chat'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # # Check we used correct template
        # self.assertTemplateUsed(response, 'catalog/bookinstance_list_borrowed_user.html')
