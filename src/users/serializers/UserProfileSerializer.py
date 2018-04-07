from rest_framework import serializers
from django.contrib.auth.models import User
from constants import GENDER_CHOICES


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="userprofile.full_name")

    class Meta:
        model = User
        fields = ('id', 'full_name')


class UserProfileListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="userprofile.full_name")
    followers_count = serializers.IntegerField(source="userprofile.followers_count")
    following_count = serializers.IntegerField(source="userprofile.following_count")

    class Meta:
        model = User
        fields = ('id', 'full_name', 'following_count', 'followers_count')


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

    @staticmethod
    def get_followers(obj):
        ids = obj.userprofile.followers
        qs = User.objects.filter(pk__in=ids)
        serializer = UserProfileListSerializer(qs, many=True)
        return serializer.data

    @staticmethod
    def get_following(obj):
        ids = obj.userprofile.following
        qs = User.objects.filter(pk__in=ids)
        serializer = UserProfileListSerializer(qs, many=True)
        return serializer.data
