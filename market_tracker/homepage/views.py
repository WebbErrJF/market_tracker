from django.shortcuts import render
from django.views import View


class HomepageView(View):
    template_name = 'homepage/home.html'

    def get(self, request, *args, **kwargs):
        context = {'title': 'Home'}
        return render(request, self.template_name, context)
