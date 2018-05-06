from rest_framework import serializers
from .models import Comment
from users.serializers.UserProfileSerializer import UserProfileSimpleSerializer
from entities.serializers import EntitySerializer
from likes.serializers import LikeSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)
    id = EntitySerializer(read_only=True)['id']
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'modified_date', 'likes')

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment
