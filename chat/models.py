import uuid
from django.db import models, IntegrityError
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models import Manager

User = get_user_model()

def uuid_without_dash():
    return uuid.uuid4().hex


class RoomManager(Manager):

    def get_or_create_room(self, user1, user2):
        if user1 == user2:
            raise ValueError("Both user cannot be same")

        qs = self.filter(Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1))
        self.filtered_qs = qs
        if qs.exists():
            if qs.count() > 1:
                qs.first().delete()
                return qs.last()

            return qs.get()

        obj = self.create(user1=user1, user2=user2)
        return obj

    def create(self, **kwargs):
        user1 = kwargs.get("user1")
        user2 = kwargs.get("user2")
        print("Users --> ", user1, user2)
        try:
            qs = self.filtered_qs
            if qs:
                raise IntegrityError("Room for with user already exists")
        except:
            pass

        qs = self.filter(Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1))
        print(qs)
        if qs.exists():
            raise IntegrityError("Room for with user already exists")

        return super().create(**kwargs)



class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid_without_dash)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user1_room")
    user2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user2_room")

    objects = RoomManager()

    class Meta:
        unique_together = ["user1", "user2"]
        ordering = ["-created", ]

    def __str__(self):
        return f"{self.user1} <-- room --> {self.user2}"


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid_without_dash)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, null=True, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_room_messages")
    text = models.TextField(null=True, blank=True)
    # image = models.CharField(max_length=2040, null=True, blank=True)
    # video = models.CharField(max_length=2040, null=True, blank=True)
    seen = models.BooleanField(default=False)
    reply = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user} {self.text}"

    class Meta:
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        
        room = self.room
        print(room)
        user = self.user
        if user not in [room.user1, room.user2]:
            raise ValueError("User is not in room.")

        return super().save(*args, **kwargs)
