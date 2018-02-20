from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User
from constants import GENDER_CHOICES


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="userprofile.full_name")

    gender = serializers.ChoiceField(
        source="userprofile.gender",
        choices=GENDER_CHOICES)

    phone_number = serializers.CharField(
        source="userprofile.phone_number")

    class Meta:
        model = User
        fields = ('id', 'full_name', 'gender', 'phone_number', 'email')
