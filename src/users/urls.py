from django.urls import path
from .views import UserProfilesAPIView

urlpatterns = [
    path('', UserProfilesAPIView.as_view()),
]