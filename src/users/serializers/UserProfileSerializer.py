from rest_framework import serializers
from users.models import Follow, UserProfile
from django.contrib.auth.models import User
from constants import GENDER_CHOICES
from .FollowSerializer import FollowSerializer


class ProfileListSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('id', 'full_name', 'following_count', 'followers_count')

    def get_followers_count(self, obj):
        qs = obj.followers

        return len(qs)

    def get_following_count(self, obj):
        qs = obj.following.count()
        return qs


class UserProfileListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="userprofile.full_name")

    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'full_name', 'following_count', 'followers_count')

    def get_followers_count(self, obj):
        qs = obj.userprofile.followers

        return len(qs)

    def get_following_count(self, obj):
        qs = obj.userprofile.following.count()
        return qs


class UserProfileDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="userprofile.full_name")

    gender = serializers.ChoiceField(
        source="userprofile.gender",
        choices=GENDER_CHOICES)

    phone_number = serializers.CharField(
        source="userprofile.phone_number")

    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'full_name', 'gender', 'phone_number', 'following', 'email', 'followers')

    def get_followers(self, obj):
        ids = obj.userprofile.followers
        qs = User.objects.filter(pk__in=ids)
        serializer = UserProfileListSerializer(qs, many=True)
        return serializer.data

    def get_following(self, obj):
        ids = obj.userprofile.following
        serializer = ProfileListSerializer(ids, many=True)
        return serializer.data