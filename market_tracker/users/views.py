from .forms import RegisterForm
from django.views.generic import FormView


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = 'users/home.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
