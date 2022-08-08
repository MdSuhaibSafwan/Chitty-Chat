from rest_framework import serializers
from ..models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_has_sent = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = "__all__"

    def get_user_has_sent(self, serializer):
        request = self.context.get("request")
        user = self.context.get("user")
        if user:
            return serializer.user == user

        if not request:
            raise serializers.ValidationError("provide request parameter in lin 15 chat/api/serializer")

        return serializer.user == request.user
