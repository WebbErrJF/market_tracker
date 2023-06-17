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
