from rest_framework import generics, permissions
from .serializers import UserProfileDetailSerializer, UserProfileListSerializer
from django.contrib.auth import get_user_model
from utils import  mixins as custom_mixins
from rest_framework.views import APIView
from utils import responses


class UserProfilesAPIView(generics.ListCreateAPIView, custom_mixins.ListModelMixin, custom_mixins.CreateModelMixin):
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileListSerializer


class UserProfileItemAPIView(generics.RetrieveAPIView, custom_mixins.RetrieveModelMixin):
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileDetailSerializer


class MeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileDetailSerializer

    @staticmethod
    def get(request):
        me = get_user_model().objects.get(pk=request.user.id)
        serializer = UserProfileDetailSerializer(me)
        return responses.successful_response(serializer.data)