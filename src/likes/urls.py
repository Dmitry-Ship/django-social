from django.urls import path
from .views import PostLikesAPIView, MyLikedCommentsAPIView, MyLikedPostsAPIView, PostDislikeAPIView

urlpatterns = [
    path('', PostLikesAPIView.as_view()),
    path('dislike', PostDislikeAPIView.as_view()),
    path('myLikedPosts', MyLikedPostsAPIView.as_view()),
    path('myLikedComments', MyLikedCommentsAPIView.as_view()),
]