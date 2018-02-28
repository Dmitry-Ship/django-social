from rest_framework import serializers
from .models import Post
from users.serializers.UserProfileSerializer import UserProfileListSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserProfileListSerializer()

    class Meta:
        model = Post
        fields = ('id', 'author', 'content')


