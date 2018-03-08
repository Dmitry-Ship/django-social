from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, mixins, permissions
from rest_framework.views import APIView
from .serializers import UserProfileDetailSerializer, UserProfileListSerializer
from django.contrib.auth.models import User
import users.errors as errors
from utils import responses, custom_mixins


class UserProfilesAPIView(generics.ListCreateAPIView, custom_mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserProfileItemAPIView(generics.RetrieveAPIView, custom_mixins.RetrieveModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileDetailSerializer
    queryset = User.objects.all()


class FollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request, pk):
        user = User.objects.get(pk=request.user.id)
        try:
            target = User.objects.get(pk=pk)
        except ObjectDoesNotExist as err:
            return responses.failed_response(err.__str__())

        try:
            user.userprofile.follow(target=target)
            return responses.successful_response()
        except errors.SelfFollowing as err:
            return responses.failed_response(err.__str__())


class UnfollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request, pk):
        user = User.objects.get(pk=request.user.id)
        try:
            target = User.objects.get(pk=pk)
        except ObjectDoesNotExist as err:
            return responses.failed_response(err.__str__())

        try:
            user.userprofile.unfollow(target=target)
        except errors.NotFollowing as err:
            return responses.failed_response(err.__str__())

        return responses.successful_response()