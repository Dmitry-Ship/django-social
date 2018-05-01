from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views import MeAPIView
from posts.views import FeedAPIView, MyPostsAPIView
from follows.views import MyFollowersAPIView, IFollowAPIView
from likes.views import MyLikesAPIView


urlpatterns = [
    path('feed/', FeedAPIView.as_view()),
    path('myposts/', MyPostsAPIView.as_view()),
    path('myfollowers/', MyFollowersAPIView.as_view()),
    path('ifollow/', IFollowAPIView.as_view()),
    path('mylikes/', MyLikesAPIView.as_view()),
    path('me/', MeAPIView.as_view()),
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('comments/', include('comments.urls')),
    path('likes/', include('likes.urls')),
    path('follows/', include('follows.urls')),
    path('users/', include('users.urls')),
    path('accounts/login/', auth_views.LoginView.as_view()),
    path('accounts/logout/', auth_views.LogoutView.as_view()),
]
