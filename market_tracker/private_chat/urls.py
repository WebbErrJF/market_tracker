from django.urls import path
from . import views

urlpatterns = [
    path("chat/<int:passed_user_id>/", views.Chat.as_view(), name="chat"),
    path("chat/", views.Chat.as_view(), name="chat")
]
