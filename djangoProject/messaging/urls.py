from django.urls import path
from .views import get_user_suggestions, inbox, send_message, sent_messages

urlpatterns = [
    path("send_message/", send_message, name="send_message"),
    path("inbox/", inbox, name="inbox"),
    path("sent/", sent_messages, name="sent_messages"),
    path("get_user_suggestions/", get_user_suggestions, name="get_user_suggestions"),
]
