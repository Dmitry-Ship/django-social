from rest_framework import serializers
from .models import Like, Target
from users.serializers.UserProfileSerializer import UserProfileSimpleSerializer


class LikeSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'author')


class TargetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Target
        fields = ['id']
