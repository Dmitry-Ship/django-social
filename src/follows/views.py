from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions, generics
from django.contrib.auth import get_user_model
from utils import responses, decorators
from .decorators import handle_follow_errors
from .models import Follow
from users.serializers import UserProfileListSerializer
from django.core.exceptions import ObjectDoesNotExist
from .errors import NotFollowing
User = get_user_model()


class FollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @handle_follow_errors
    def post(request):
        user = get_object_or_404(User, pk=request.user.id)
        target = get_object_or_404(User, pk=request.data['user'])
        Follow.objects.create(to_person=target, from_person=user)

        return responses.successful_response()


class UnfollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @handle_follow_errors
    def post(request):
        user = get_object_or_404(User, pk=request.user.id)
        target = get_object_or_404(User, pk=request.data['user'])

        try:
            follow = Follow.active.get(to_person=target, from_person=user)
        except ObjectDoesNotExist:
            raise NotFollowing

        follow.deactivate()
        follow.save()

        return responses.successful_response()


@responses.successful_response_decorator
class IFollowAPIView(generics.ListAPIView):
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        users = Follow.active.filter(from_person=self.request.user).values_list('to_person')
        return User.objects.filter(id__in=users)


@responses.successful_response_decorator
class MyFollowersAPIView(generics.ListAPIView):
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        users = Follow.active.filter(to_person=self.request.user).values_list('from_person')
        return User.objects.filter(id__in=users)


@responses.successful_response_decorator
class FollowersAPIView(generics.ListAPIView):
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @decorators.require_parameter('user')
    def get_queryset(query):
        users = Follow.active.filter(to_person=query).values_list('from_person')
        return User.objects.filter(id__in=users)


@responses.successful_response_decorator
class FollowingAPIView(generics.ListAPIView):
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.require_parameter('user')
    def get_queryset(self, query):
        users = Follow.active.filter(from_person=query).values_list('to_person')
        return User.objects.filter(id__in=users)

