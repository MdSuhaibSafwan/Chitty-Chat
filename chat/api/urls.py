from django.urls import path
from .views import get_user_rooms

urlpatterns = [
    path("user/room/", get_user_rooms),
]
