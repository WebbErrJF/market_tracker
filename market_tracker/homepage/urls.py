from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomepageView.as_view(), name='homepage'),
    path('about/', views.AboutView.as_view(), name='about')
]
