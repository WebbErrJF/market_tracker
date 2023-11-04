from django.shortcuts import render
from django.views import View
from .models import UserContact
from django.contrib.auth.mixins import LoginRequiredMixin


class Chat(LoginRequiredMixin, View):
    template_name = "private_chat/chat.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        user_contacts = UserContact.objects.filter(user=user).values_list('contact__username', 'contact__id', flat=False)

        passed_user_id = kwargs.get('passed_user_id', None)
        if passed_user_id:
            contact, created = UserContact.objects.get_or_create(user=user, contact_id=passed_user_id)
            if created:
                user_contacts = list(user_contacts) + [(contact.contact.username, contact.contact.id)]

        context = {
            'logged_user': str(user),
            'contacts': user_contacts,
            'passed_user': passed_user_id or '',
        }
        return render(request, self.template_name, context)
