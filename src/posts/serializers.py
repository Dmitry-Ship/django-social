from rest_framework import serializers
from .models import Post
from users.serializers.UserProfileSerializer import UserProfileSimpleSerializer
from comments.serializers import CommentSerializer
from likes.serializers import LikeSerializer
from entities.serializers import EntitySerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    id = EntitySerializer(read_only=True)['id']

    class Meta:
        model = Post
        fields = ('author', 'content', 'modified_date', 'comments', 'likes')

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post
