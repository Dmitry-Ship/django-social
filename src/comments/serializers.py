from rest_framework import serializers
from .models import Comment
from users.serializers.UserProfileSerializer import UserProfileListSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserProfileListSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'modified_date')

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment
