import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Добавляем WebSocket-маршрутизатор для обработки запросов WebSocket
    "websocket": AuthMiddlewareStack(
        URLRouter(
            # URL-шаблоны WebSocket-обработчиков
        )
    ),
})
