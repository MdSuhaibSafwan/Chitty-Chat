from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from .models import ChatRoom, ChatMessage


def index(request):
    if not request.user.is_authenticated:
        # return redirect("")
        return 

    token_obj, created = Token.objects.get_or_create(user=request.user)

    context = {
        "token": token_obj.key,
    }

    return render(request, "chat/index.html", context)
