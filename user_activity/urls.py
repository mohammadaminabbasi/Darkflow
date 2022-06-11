from django.urls import path
from rest_framework import routers

from user_activity.views import *

router = routers.DefaultRouter()

urlpatterns = [
    path('like_song/', like_song, name="like_song"),
    path('unlike_song/', unlike_song, name="unlike_song"),
    path('is_song_liked_by_user/', is_song_liked_by_user, name="is_song_liked_by_user"),
    path('comment_song/', comment_song, name="comment_song"),
    path('get_all_song_comments/', get_all_song_comments, name="comment_song"),
]
