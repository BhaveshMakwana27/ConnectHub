import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from Messaging.models import Message
from Accounts.models import UserProfile
from django.contrib.auth.models import User
from datetime import datetime,timedelta
import pytz

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, 
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, 
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        receiver = text_data_json["receiver"]

        # save message

        self.save_message(message,username,receiver) 

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat.message", 
                "message": message,
                "username": username,
                "receiver": receiver
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        receiver = event["receiver"]
        # Send message to WebSocket
        self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                    "receiver": receiver
                }
            )
        )
    
    def save_message(self,message,username,receiver):
        user = User.objects.get(username=username)
        receiverUser = User.objects.get(username=receiver)
        senderName = UserProfile.objects.get(user=user)
        receiverName = UserProfile.objects.get(user=receiverUser)

        # message current time
        timezone = pytz.timezone('Asia/Kolkata')
        currTime = datetime.now(timezone)+ timedelta(hours=5, minutes=30)
        Message.objects.create(sender=senderName,receiver=receiverName,content=message,timeStamp=currTime )