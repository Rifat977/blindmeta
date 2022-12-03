import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
import pyttsx3
from .models import Message, Room
from django.contrib.auth.models import User
import asyncio


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
  

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        sentByUser = text_data_json['sentByUser']
        room = text_data_json['room']

        self.save_message(username, room, message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'username':username,
                'sentByUser': sentByUser,
                'room':room
            }
        )


    def chat_message(self, event):
        message = event['message']
        username = event['username']
        sentByUser = event['sentByUser']
        room = event['room']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'username':username,
            'sentByUser':sentByUser,
            'room':room
        }))  
        audio = pyttsx3.init()
        audio.setProperty("rate", 130)
        audio.say(message)
        audio.runAndWait()
        audio.stop()

    def save_message(self, username, room, message):
            user = User.objects.get(username=username)
            room = Room.objects.get(slug=room)
            Message.objects.create(user=user, room=room, content=message)