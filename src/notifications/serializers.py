from rest_framework import serializers
from .models import Notification, NotificationPostLiked
from posts.serializers import PostNotificationSerializer
from comments.serializers import CommentNotificationSerializer
from users.serializers.UserProfileSerializer import UserProfileSimpleSerializer
from .constans import TYPE_CHOICES


class NotificationSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'author', 'type')


class NotificationPostLikedSerializer(serializers.ModelSerializer):
    post = PostNotificationSerializer(read_only=True)
    type = serializers.ChoiceField(choices=TYPE_CHOICES,source="notification.type")
    author = UserProfileSimpleSerializer(source="notification.author", read_only=True)

    class Meta:
        model = NotificationPostLiked
        fields = ('post', 'type', 'author')


class NotificationCommentLikedSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=TYPE_CHOICES,source="notification.type")
    author = UserProfileSimpleSerializer(source="notification.author", read_only=True)
    comment = CommentNotificationSerializer(read_only=True)

    class Meta:
        model = NotificationPostLiked
        fields = ('type', 'author', 'comment')


class NotificationPostCommentedSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=TYPE_CHOICES,source="notification.type")
    author = UserProfileSimpleSerializer(source="notification.author", read_only=True)
    post = PostNotificationSerializer(read_only=True)
    comment = CommentNotificationSerializer(read_only=True)

    class Meta:
        model = NotificationPostLiked
        fields = ('type', 'author', 'post', 'comment')


class NotificationFollowedSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=TYPE_CHOICES,source="notification.type")
    author = UserProfileSimpleSerializer(source="notification.author", read_only=True)

    class Meta:
        model = NotificationPostLiked
        fields = ('type', 'author')
