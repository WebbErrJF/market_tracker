from django.urls import path
from . import views

urlpatterns = [
    path("blog/", views.MainPage.as_view(), name="blog"),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
]
