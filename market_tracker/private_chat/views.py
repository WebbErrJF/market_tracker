from django.shortcuts import render
from django.views import View
from .models import UserContact


class Chat(View):
    template_name = "private_chat/chat.html"

    def get(self, request, *args, **kwargs):
        user_contacts = list(UserContact.objects.filter(user=request.user).values_list('contact__username',
                                                                                       'contact__id', flat=False))
        user = str(request.user)
        context = {'user': user,
                   'contacts': user_contacts}
        return render(request, self.template_name, context)
