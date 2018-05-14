from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.constants import GENDER_CHOICES
from ..models import UserProfile


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="userprofile.full_name")

    class Meta:
        model = get_user_model()
        fields = ('id', 'full_name')


class UserProfileListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField()
    followers_count = serializers.IntegerField()

    class Meta:
        model = UserProfile
        fields = ('id', 'full_name', 'followers_count')


class UserProfileDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="userprofile.full_name", required=False, read_only=True)

    gender = serializers.ChoiceField(
        source="userprofile.gender",
        choices=GENDER_CHOICES, required=False)

    phone_number = serializers.CharField(
        source="userprofile.phone_number", required=False)

    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'full_name', 'gender', 'phone_number', 'following', 'followers')

    @staticmethod
    def get_followers(obj):
        ids = obj.userprofile.followers
        qs = get_user_model().objects.filter(pk__in=ids)
        serializer = UserProfileListSerializer(qs, many=True)
        return serializer.data

    @staticmethod
    def get_following(obj):
        ids = obj.userprofile.following
        qs = get_user_model().objects.filter(pk__in=ids)
        serializer = UserProfileListSerializer(qs, many=True)
        return serializer.data


class UserUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(
        choices=GENDER_CHOICES, required=False)

    phone_number = serializers.CharField(required=False)

    user = UserUpdateSerializer()

    class Meta:
        model = UserProfile
        fields = ('gender', 'phone_number', 'user')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()

        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.save()

        return instance


