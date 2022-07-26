import json
from .models import ChatRoom, ChatMessage
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


@sync_to_async
def get_room(user1, user2):
    room = ChatRoom.objects.get_or_create_room(user1, user2)
    return room


@sync_to_async
def save_message(room, message_dict, user):
    print(message_dict)
    message_obj = ChatMessage(post=message_dict.get("post"), text=message_dict.get("text"))
    message_obj.user = user
    message_obj.room = room
    message_obj.save()

    print("MESSAGED SAVED")


@sync_to_async
def save_edited_message(message_id, message_dict):
    try:
        chat_msg_obj = ChatMessage.objects.get(id=message_id)
    except ObjectDoesNotExist:
        raise ValueError("Message object does not exists")

    chat_msg_obj.text = message_dict.text
    chat_msg_obj.save()
    return chat_msg_obj


@sync_to_async
def delete_message(message_id):
    try:
        chat_msg_obj = ChatMessage.objects.get(id=message_id)
    except ObjectDoesNotExist:
        return False

    chat_msg_obj.delete()
    return True


@sync_to_async
def authenticate_by_token(token):
    pass


@sync_to_async
def get_user_by_username(username):
    if "@" in username:
        qs = User.objects.filter(email=username)
    else:
        qs = User.objects.filter(username=username)
    
    if qs.exists():
        return qs.get()

    return False


def get_all_messages(room_id):
    try:
        room = ChatRoom.objects.get(room__id=room_id)
    except ObjectDoesNotExist:
        raise ValueError("Chat Room does not exists")
    
    return room.messages.all()

