import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, ChatMessage
from .utils import get_room, save_message, save_edited_message, authenticate_by_token, \
    get_user_by_username


class ChatConsumer(AsyncConsumer):
    # room = None
    # auth_user = None

    async def fetch_messages(self, data):
        print(data)
    #     messages = await get_last_messages(self.room)
    
    #     content = {
    #         'command': 'messages',
    #         'messages': await self.messages_to_json(messages)
    #     }
    #     data = {}
    #     data["data"] = content
    #     await self.send_message(data)

    # async def messages_to_json(self, messages):
    #     result = []
    #     for message in messages:
    #         result.append(await self.message_to_json(message))
    #     return result

    # async def message_to_json(self, message):
    #     # data =  MessageSerializer(message).data
    #     try:
    #         data = {
               
    #             "id": str(message.id),
    #             'author': message.user.username,
    #             'content': message.text,
    #             "image": message.image,
    #             "video": message.video,
    #             "reply": message.reply,
    #             "seen": message.seen,
    #             'timestamp': str(message.timestamp)
    #         }
    #     except AttributeError as e:
    #         print("Error ", e)
    #         return None
    #     if data["reply"] is not None:
    #         data["reply"] = str(data["reply"].id)

    #     return data

    async def new_message(self, data):
        print(data, "inside new message")
        msg_dict = {
            "post": data.get("post"),
            "text": data.get("text"),
        }
        await save_message(self.room, msg_dict, self.scope["user"])

    #     try:
    #         await send_message_online(self.room, self.auth_user, data['message'],
    #                                 data.get("image"), data.get("video"), data.get("reply"),data.get('partner'),data.get('notify_message'))
    #     except KeyError as e:
    #         print("Error ", e)
    #         return

    async def delete_message(self, data):
        message_id = data["message_id"]
    #     obj = await get_message_by_id(message_id)
    #     if obj == None:
    #         await self.send({
    #             "type": "websocket.close"
    #         })

    #         return

    #     await delete_message_obj(obj)
    #     return obj


    async def edit_message(self, data):
        message_id = data["message_id"]
    #     print(message_id)
    #     new_msg = data["message"]
    #     obj = await get_message_by_id(message_id)
    #     print(obj)
    #     img = data.get("image")
    #     video = data.get("video")
    #     reply = data.get("reply")
    #     return await self.save_edited_message(message_obj=obj, new_msg=new_msg, image=img, video=video, reply=reply)

    @database_sync_to_async
    def save_edited_message(self, message_obj, new_msg, image, video, reply):
        message_obj.text = new_msg
        message_obj.image = image
        message_obj.video = video
        message_obj.reply = reply
        message_obj.save()


    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'delete_message': delete_message,
        "edit_message": edit_message,
    }

    async def websocket_connect(self, event):
        print("Connected ", event)

        await self.send({
            "type": "websocket.accept",
        })

        curr_user = self.scope["user"]
        print(curr_user)
        
        if not curr_user.is_authenticated:
            print("User is not Authenticated")
            await self.send({
                "type": "websocket.close"
            })
            return 
        chat_room = f"room_{curr_user.id}"
        self.room = chat_room
        self.auth_user = curr_user
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

    @database_sync_to_async
    def save_message(self, room, text, reply=None):
        user = self.scope["user"]
        obj = ChatMessage.objects.create(user=user, reply=reply, room=room, text=text)
        return obj

    async def send_message(self, event):
        print(event)
        data = json.dumps(event["data"])
        print("Inside Send message ", data)
        print("Sending Message data Via Consumers")
        await self.send({
            "type": "websocket.send",
            "text": data,
        })

    async def websocket_receive(self, event):
        print("Received ", event)
        data = json.loads(event["text"])
        print(data)
        try:
            await self.commands[data['command']](self, data) # either fetch_messages or new_message
        except KeyError as k:
            print("Error ", k)

    async def websocket_disconnect(self, event):
        print("Disconnected ", event)
