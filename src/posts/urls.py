from django.urls import path
from .views import PostItemAPIView, PostsAPIView

urlpatterns = [
    path('', PostsAPIView.as_view()),
    # path('recent', RecentPostsAPIView.as_view()),
    # path('<int:pk>', PostItemAPIView.as_view()),
]