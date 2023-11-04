from django.test import TestCase
from django.urls import reverse_lazy
from homepage.tests.views.client import test_client


class TestHomepageView(TestCase):
    def test_should_return_status_code_200(self):
        expected_status_code = 200
        resp = test_client.get(reverse_lazy("homepage"))
        actual_status_code = resp.status_code

        self.assertEquals(expected_status_code, actual_status_code)

    def test_should_return_valid_template(self):
        expected_template_path = "homepage/home.html"
        resp = test_client.get(reverse_lazy("homepage"))
        actual_template_path = resp.templates[0].name

        self.assertEqual(actual_template_path, expected_template_path)

    def test_should_return_valid_context(self):
        expected_context = 'Home'
        resp = test_client.get(reverse_lazy("homepage"))
        actual_context = resp.context['title']

        self.assertEquals(actual_context, expected_context)
