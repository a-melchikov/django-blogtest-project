from django.shortcuts import render
from django.views.generic import TemplateView


class ChatPageView(TemplateView):
    template_name = "chat/chat.html"


def chat_view(request, room_name):
    return render(
        request, "chat/chat.html", {"room_name": room_name, "user": request.user}
    )
