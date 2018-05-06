from rest_framework import serializers
from .models import Like
from users.serializers.UserProfileSerializer import UserProfileSimpleSerializer


class LikeSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'author')

