from rest_framework import serializers
from .models import Post
from users.serializers.UserProfileSerializer import UserProfileListSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserProfileListSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'modified_date')

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post
