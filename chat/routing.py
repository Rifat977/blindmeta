from django.urls import re_path 
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/group/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/user/(?P<user_name>[^/]+)/$', consumers.ChatConsumer.as_asgi())
]