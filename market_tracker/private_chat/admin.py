from django.contrib import admin

from .models import Message, UserContact

admin.site.register(Message)
admin.site.register(UserContact)
