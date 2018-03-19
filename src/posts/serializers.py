from rest_framework import serializers
from .models import Post
from users.serializers.UserProfileSerializer import UserProfileListSerializer
from comments.serializers import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserProfileListSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'modified_date', 'comments')

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post
