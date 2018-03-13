from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, mixins, permissions
from rest_framework.views import APIView
from .serializers import UserProfileDetailSerializer, UserProfileListSerializer
from django.contrib.auth.models import User
import users.errors as errors
from utils import responses, mixins as custom_mixins
from utils.decorators import custom_404


class UserProfilesAPIView(generics.ListCreateAPIView, custom_mixins.ListModelMixin, custom_mixins.CreateModelMixin):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileListSerializer


class UserProfileItemAPIView(generics.RetrieveAPIView, custom_mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileDetailSerializer


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
    @custom_404
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