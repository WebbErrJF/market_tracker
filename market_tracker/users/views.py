from django.shortcuts import render

from .forms import RegisterForm
from django.views.generic import FormView
from django.urls import reverse_lazy


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('login')


def dashboard(request):
    return render(request, 'users/dashboard.html', {'title': 'Dashboard'})


def stock_list(request):
    return render(request, 'users/stock_list.html', {'title': 'Stock list data'})


def profile(request):
    return render(request, 'users/profile.html', {'title': 'User profile'})