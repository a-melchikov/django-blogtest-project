from django.urls import path
from .views import get_user_suggestions, inbox, send_message

urlpatterns = [
    path("send_message/", send_message, name="send_message"),
    path("inbox/", inbox, name="inbox"),
    path("get_user_suggestions/", get_user_suggestions, name="get_user_suggestions"),
]
