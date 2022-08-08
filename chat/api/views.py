from django.db.models import Q
from rest_framework.decorators import api_view
from .serializers import ChatMessageSerializer
from ..models import ChatRoom, ChatMessage
from user.api.serializers import UserForRoomSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model; User = get_user_model()


@api_view(["GET", ])
def get_user_rooms(request):
    user = request.user

    qs = User.objects.filter(Q(user1_room__user2=user) | Q(user2_room__user1=user))
    serializer = UserForRoomSerializer(qs, many=True)
    serializer.context["request"] = request

    return Response(serializer.data, status=200)
