from rest_framework import serializers
from .models import Comment
from users.serializers.UserProfileSerializer import UserProfileSimpleSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'modified_date')

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment
