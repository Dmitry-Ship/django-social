from rest_framework import serializers
from .models import PostLike, CommentLike
from users.serializers.UserProfileSerializer import UserProfileSimpleSerializer


class PostLikeSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = ('id', 'author')


class CommentLikeSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = ('id', 'author')