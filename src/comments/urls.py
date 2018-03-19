from django.urls import path
from .views import CommentItemAPIView, CommentsAPIView

urlpatterns = [
    path('', CommentsAPIView.as_view()),
    path('<int:pk>', CommentItemAPIView.as_view()),
]