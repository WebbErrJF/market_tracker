from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', extra_context={'title': 'Login'}),
         name='login'),
    path('register/', views.RegisterView.as_view(extra_context={'title': 'Register'}), name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('stock-list/', views.stock_list, name='stock_list'),
    path('profile/', views.profile, name='profile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
