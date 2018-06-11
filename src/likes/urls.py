from django.urls import path
from .views import PostLikesAPIView, CommentLikesAPIView, MyLikedCommentsAPIView, MyLikedPostsAPIView, PostDislikeAPIView

urlpatterns = [
    path('post', PostLikesAPIView.as_view()),
    path('comment', CommentLikesAPIView.as_view()),
    path('dislike', PostDislikeAPIView.as_view()),
    path('myLikedPosts', MyLikedPostsAPIView.as_view()),
    path('myLikedComments', MyLikedCommentsAPIView.as_view()),
]