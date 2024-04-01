import os
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.consumers import ChatConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # Добавляем WebSocket-маршрутизатор для обработки запросов WebSocket
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("chat/<str:room_name>/", ChatConsumer.as_asgi()),
                ]
            )
        ),
    }
)
