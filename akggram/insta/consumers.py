# import asyncio
# import json
# from django.contrib.auth import get_user_model
# from channels.consumer import AsyncConsumer
# from channels.db import database_sync_to_async
# from .models import Thread ,ChatMessage

# class ChatConsumer(AsyncConsumer):
#     async def websocket_connect(self,event):
#         print ('connected', event)
        
#     async def websocket_receive(self,event):
#         print ('receive', event)

#     async def websocket_disconnect(self,event):
#         print ('disconnect', event)   
#chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        })) 