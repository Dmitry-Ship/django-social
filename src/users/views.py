from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import permissions, generics
from .serializers import UserProfileDetailSerializer, UserProfileListSerializer, UserProfileUpdateSerializer
from .forms import SignUpForm
from .models import UserProfile
from utils import responses, pagination
User = get_user_model()


@responses.successful_response_decorator
class UserProfilesAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileListSerializer
    # pagination_class = pagination.StandardResultsSetPagination


@responses.successful_response_decorator
class UserProfileItemAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileDetailSerializer


@responses.successful_response_decorator
class MeAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileDetailSerializer

    def get_object(self):
        return User.objects.get(pk=self.request.user.id)


@responses.successful_response_decorator
class MeUpdateAPIView(generics.UpdateAPIView):
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