from django.contrib import admin

from .models import Profile, SubscribedCompanies

admin.site.register(Profile)
admin.site.register(SubscribedCompanies)
