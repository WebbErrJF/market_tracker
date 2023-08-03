from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.avif', upload_to='profile_pics')
    description = models.TextField(help_text='Describe yourself in few words')

    def __str__(self):
        return str(self.user.username)

