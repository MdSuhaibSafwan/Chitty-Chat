import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .middleware import TokenAuthMiddleware
from django.urls import path
from django.core.asgi import get_asgi_application
from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path("room/", ChatConsumer.as_asgi(), ),
]

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

application = ProtocolTypeRouter(
    {
        # "http": get_asgi_application(),
        "websocket": TokenAuthMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
