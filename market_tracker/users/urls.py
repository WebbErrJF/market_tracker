from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', extra_context={'title': 'Login'}),
         name='login'),
    path('register/', views.RegisterView.as_view(extra_context={'title': 'Register'}), name='register'),
    path('dashboard/', views.profile, name='dashboard'),
    path('stock-list/', views.stock_list, name='stock_list')
]
