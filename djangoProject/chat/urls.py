from django.urls import path
from .views import ChatPageView, chat_view

urlpatterns = [
    path("", ChatPageView.as_view(), name="chat"),
    path("<str:room_name>/", chat_view, name="chat_room"),
]
