from django.urls import path
from .views import LikesAPIView, MyLikedCommentsAPIView, MyLikedPostsAPIView, DislikeAPIView

urlpatterns = [
    path('', LikesAPIView.as_view()),
    path('dislike', DislikeAPIView.as_view()),
    path('myLikedPosts', MyLikedPostsAPIView.as_view()),
    path('myLikedComments', MyLikedCommentsAPIView.as_view()),
]