from rest_framework import generics, permissions
from .serializers import UserProfileDetailSerializer, UserProfileListSerializer
from django.contrib.auth.models import User
from utils import  mixins as custom_mixins
from rest_framework.views import APIView
from utils import responses


class UserProfilesAPIView(generics.ListCreateAPIView, custom_mixins.ListModelMixin, custom_mixins.CreateModelMixin):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileListSerializer


class UserProfileItemAPIView(generics.RetrieveAPIView, custom_mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileDetailSerializer


class MeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileDetailSerializer

    @staticmethod
    def get(request):
        me = User.objects.get(pk=request.user.id)
        serializer = UserProfileDetailSerializer(me)
        return responses.successful_response(serializer.data)