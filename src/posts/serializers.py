from .models import Post
from users.serializers.UserProfileSerializer import UserProfileSimpleSerializer
from comments.serializers import CommentSerializer
from likes.serializers import PostLikeSerializer
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = PostLikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'modified_date', 'comments', 'likes')

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post


class PostNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id',  'content')
