from django.urls import path
from rest_framework import routers

from user_activity.views import *

router = routers.DefaultRouter()

urlpatterns = [
    path('like_song/', like_song, name="like_song"),
    path('unlike_song/', unlike_song, name="unlike_song"),
    path('comment_song/', comment_song, name="comment_song"),
]
