from django.test import TestCase
from django.urls import reverse_lazy
from blog.tests.views.client import test_client
from django.contrib.auth.models import User
from blog.models import Article, Comment
import json


class TestCommentAPI(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.test_user = User.objects.create_user(username=self.username, password=self.password)
        self.test_article = Article.objects.create(
            author=self.test_user,
            title="test title",
            content="test content",
            description="Test description"
        )
        self.test_comment = Comment.objects.create(
            author=self.test_user,
            content="Test content",
            article_id=self.test_article
        )

    def test_should_return_status_code_200_when_its_posted_valid_comment(self):
        expected_status_code = 201
        data = {
            'content': 'Test comment content',
            'author': self.test_user.id,
            'article_id': self.test_article.id
        }
        login = test_client.login(username=self.username, password=self.password)
        resp = test_client.post(reverse_lazy('comments_api'), data)

        self.assertEqual(resp.status_code, expected_status_code)

    def test_should_return_status_code_400_when_its_posted_invalid_comment(self):
        expected_status_code = 400
        data = {"test": "test"}
        login = test_client.login(username=self.username, password=self.password)
        resp = test_client.post(reverse_lazy('comments_api'), data)

        self.assertEqual(resp.status_code, expected_status_code)

    def test_should_return_status_code_200_when_its_patched_valid_comment(self):
        expected_status_code = 201
        test_data = json.dumps({'content': 'Updated comment content'})
        url = reverse_lazy('comments_api', kwargs={'pk': self.test_comment.pk})
        response = test_client.patch(url, test_data, content_type='application/json')

        self.assertEqual(response.status_code, expected_status_code)
        self.test_comment.refresh_from_db()
        self.assertEqual(self.test_comment.content, 'Updated comment content')

    def test_should_return_status_code_400_when_its_patched_invalid_comment(self):
        test_data = json.dumps({'wrong_key': 'Updated comment content'})
        url = reverse_lazy('comments_api', kwargs={'pk': self.test_comment.pk})
        response = self.client.patch(url, data=test_data, content_type='application/json')
        self.test_comment.refresh_from_db()
        self.assertNotEquals(self.test_comment.content, 'Updated comment content')

    def test_should_return_status_code_204_when_comment_is_deleted(self):
        initial_count = Comment.objects.count()
        expected_status_code = 204
        url = reverse_lazy('comments_api', kwargs={'pk': self.test_comment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(Comment.objects.count(), initial_count - 1)
