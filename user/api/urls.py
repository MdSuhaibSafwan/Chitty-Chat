from django.urls import path
from .views import CustomAuthToken

urlpatterns = [
    path("obtain-token/", CustomAuthToken.as_view(), )
]
