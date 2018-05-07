from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .serializers import UserProfileDetailSerializer, UserProfileListSerializer
from utils import mixins as custom_mixins
from rest_framework.views import APIView
from utils import responses
from .forms import SignUpForm


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


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'users/signedup.html')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})