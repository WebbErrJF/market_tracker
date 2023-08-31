from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', extra_context={'title': 'Login'}),
         name='login'),
    path('register/', views.RegisterView.as_view(extra_context={'title': 'Register'}), name='register'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('stock-list/', views.StockListView.as_view(), name='stock_list'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('stream/', views.StreamView.as_view(), name='stream'),
    path('subscriptions/', views.GetAllStockCompanies.as_view(), name='get_subscriptions'),
    path('initial-data/', views.GetInitialData.as_view(), name='initial_data')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
