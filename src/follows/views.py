from rest_framework.views import APIView
from rest_framework import permissions, generics
from django.contrib.auth import get_user_model
from utils import responses
from utils.decorators import handle_404
from .decorators import handle_follow_errors
from .models import Follow
from users.serializers import UserProfileListSerializer
from django.core.exceptions import ObjectDoesNotExist
from .errors import NotFollowing
from utils import mixins as custom_mixins, decorators


class FollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @handle_404
    @handle_follow_errors
    def post(request):
        user = get_user_model().objects.get(pk=request.user.id)
        target = get_user_model().objects.get(pk=request.data['user'])
        Follow.objects.create(to_person=target, from_person=user)

        return responses.successful_response()


class UnfollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @handle_404
    @handle_follow_errors
    def post(request):
        user = get_user_model().objects.get(pk=request.user.id)

        target = get_user_model().objects.get(pk=request.data['user'])

        try:
            follow = Follow.active.get(to_person=target, from_person=user)
        except ObjectDoesNotExist:
            raise NotFollowing

        follow.deactivate()
        follow.save()

        return responses.successful_response()


class IFollowAPIView(generics.ListAPIView, custom_mixins.ListModelMixin):
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        users = Follow.active.filter(from_person=self.request.user).values_list('to_person')
        return get_user_model().objects.filter(id__in=users)


class MyFollowersAPIView(generics.ListAPIView, custom_mixins.ListModelMixin):
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        users = Follow.active.filter(to_person=self.request.user).values_list('from_person')
        return get_user_model().objects.filter(id__in=users)


class FollowersAPIView(generics.ListAPIView, custom_mixins.ListModelMixin):
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.require_parameter('user')
    def get_queryset(self, query):
        users = Follow.active.filter(to_person=query).values_list('from_person')
        return get_user_model().objects.filter(id__in=users)


class FollowingAPIView(generics.ListAPIView, custom_mixins.ListModelMixin):
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.require_parameter('user')
    def get_queryset(self, query):
        users = Follow.active.filter(from_person=query).values_list('to_person')
        return get_user_model().objects.filter(id__in=users)

