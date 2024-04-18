from django.urls import path
from .views import ChatPageView, chat_view, create_room

urlpatterns = [
    path("", ChatPageView.as_view(), name="chat"),
    path("create-room/", create_room, name="create_room"),
    path("<str:room_name>/", chat_view, name="chat_room"),
]
