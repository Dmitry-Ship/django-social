from .models import PostComment
from users.serializers.UserProfileSerializer import UserProfileSimpleSerializer
from likes.serializers import CommentLikeSerializer
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)
    likes = CommentLikeSerializer(many=True, read_only=True)

    class Meta:
        model = PostComment
        fields = ('id', 'author', 'content', 'modified_date', 'likes')

    def create(self, validated_data):
        comment = PostComment.objects.create(**validated_data)
        return comment
