from django.urls import path
from .views import  MeAPIView


urlpatterns = [
    path('', MeAPIView.as_view()),
]