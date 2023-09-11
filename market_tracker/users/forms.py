from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from .models import Profile
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4})
        }
