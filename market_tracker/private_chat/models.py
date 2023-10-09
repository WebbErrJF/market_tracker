from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    thread_name = models.CharField(max_length=200)
    time_stamp = models.DateTimeField()


class UserContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contact")
