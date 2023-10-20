from django.urls import path
from . import views

urlpatterns = [
    path("blog/", views.MainPage.as_view(), name="blog"),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('comment/<int:pk>/',  views.CommentAPI.as_view(), name='comments_api'),
    path('comment/',  views.CommentAPI.as_view(), name='comments_api'),
    path('article/new/', views.ArticleCreateView.as_view(), name='article-create'),
    path('article/update/<int:pk>/', views.ArticleUpdateView.as_view(), name='article-update'),
    path('article/delete/<int:pk>/', views.ArticleDeleteView.as_view(), name='article-delete')
]
