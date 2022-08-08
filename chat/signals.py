from django.dispatch import receiver
from django.contrib.auth import get_user_model; User = get_user_model()
from .models import ChatRoom, ChatMessage
from django.db.models.signals import post_save
from asgiref.sync import sync_to_async, async_to_sync
from channels.layers import get_channel_layer
from .api.serializers import ChatMessageSerializer

channel_layer = get_channel_layer()


@receiver(signal=post_save, sender=ChatMessage)
def send_message_to_room(sender, instance, created, **kwargs):
    if created:
        print("Here", instance)
        user1 = instance.room.user1
        user2 = instance.room.user2

        serializer = ChatMessageSerializer(instance=instance)
        serializer.context["user"] = user1
        data = serializer.data
        data["room"] = str(data["room"])

        async_to_sync(channel_layer.group_send)(f"room_{user1.id}", {
            "type": "send.message",
            "data": data
        })

        serializer = ChatMessageSerializer(instance=instance)
        serializer.context["user"] = user2
        data = serializer.data
        data["room"] = str(data["room"])

        async_to_sync(channel_layer.group_send)(f"room_{user2.id}", {
            "type": "send.message",
            "data": data
        })
