# chat/routing.py
from django.urls import re_path

from Messaging import consumers

websocket_urlpatterns = [
    re_path(r"ws/messaging/do_message/(?P<room_name>[\w-]+)/$", consumers.ChatConsumer.as_asgi()),
]