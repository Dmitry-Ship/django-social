from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .serializers import UserProfileDetailSerializer, UserProfileListSerializer, UserProfileUpdateSerializer, UserUpdateSerializer
from utils import mixins as custom_mixins
from .forms import SignUpForm
from .models import UserProfile


class UserProfilesAPIView(generics.ListCreateAPIView, custom_mixins.ListModelMixin, custom_mixins.CreateModelMixin):
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileListSerializer


class UserProfileItemAPIView(generics.RetrieveAPIView, custom_mixins.RetrieveModelMixin):
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileDetailSerializer


class MeAPIView(generics.RetrieveUpdateAPIView, custom_mixins.RetrieveModelMixin, custom_mixins.UpdateModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileDetailSerializer
    lookup_field = 'pk'

    def get_object(self):
        return get_user_model().objects.get(pk=self.request.user.id)


class MeUpdateAPIView(generics.UpdateAPIView, custom_mixins.UpdateModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileUpdateSerializer

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user.id)


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