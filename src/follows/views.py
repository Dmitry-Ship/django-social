from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth import get_user_model
from utils import responses
from utils import generics as custom_generics, decorators
from .decorators import handle_follow_errors
from .models import Follow
from users.serializers import UserProfileListSerializer
from django.core.exceptions import ObjectDoesNotExist
from .errors import NotFollowing
User = get_user_model()


class FollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @decorators.handle_404
    @handle_follow_errors
    def post(request):
        user = User.objects.get(pk=request.user.id)
        target = User.objects.get(pk=request.data['user'])
        Follow.objects.create(to_person=target, from_person=user)

        return responses.successful_response()


class UnfollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @decorators.handle_404
    @handle_follow_errors
    def post(request):
        user = User.objects.get(pk=request.user.id)

        target = User.objects.get(pk=request.data['user'])

        try:
            follow = Follow.active.get(to_person=target, from_person=user)
        except ObjectDoesNotExist:
            raise NotFollowing

        follow.deactivate()
        follow.save()

        return responses.successful_response()


class IFollowAPIView(custom_generics.ListAPIView):
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        users = Follow.active.filter(from_person=self.request.user).values_list('to_person')
        return User.objects.filter(id__in=users)


class MyFollowersAPIView(custom_generics.ListAPIView):
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        users = Follow.active.filter(to_person=self.request.user).values_list('from_person')
        return User.objects.filter(id__in=users)


class FollowersAPIView(custom_generics.ListAPIView):
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @decorators.require_parameter('user')
    def get_queryset(query):
        users = Follow.active.filter(to_person=query).values_list('from_person')
        return User.objects.filter(id__in=users)


class FollowingAPIView(custom_generics.ListAPIView):
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.require_parameter('user')
    def get_queryset(self, query):
        users = Follow.active.filter(from_person=query).values_list('to_person')
        return User.objects.filter(id__in=users)

