from django.shortcuts import render
from django.views import View
from .models import UserContact
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class Chat(LoginRequiredMixin, View):
    template_name = "private_chat/chat.html"

    def get(self, request, *args, **kwargs):
        user_contacts = list(UserContact.objects.filter(user=request.user).values_list('contact__username',
                                                                                       'contact__id', flat=False))

        user = str(request.user)
        if 'passed_user_id' in kwargs.keys():

            exists = False
            for contact in user_contacts:
                if contact[1] == kwargs['passed_user_id']:
                    exists = True
            if not exists:
                contact_obj = User.objects.get(id=kwargs['passed_user_id'])
                UserContact.objects.create(user=request.user, contact=contact_obj)
                user_contacts.append((contact_obj.username, contact_obj.id))

            context = {'logged_user': user,
                       'contacts': user_contacts,
                       'passed_user': kwargs['passed_user_id']}
        else:
            context = {'logged_user': user,
                       'contacts': user_contacts,
                       'passed_user': ''}
        return render(request, self.template_name, context)
