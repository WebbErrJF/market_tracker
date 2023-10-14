from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    description = models.TextField(max_length=150)
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
