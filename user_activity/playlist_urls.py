from django.urls import path
from rest_framework import routers

from user_activity.create_random_data import user_listen_randomly
from user_activity.playlist_views import *
from user_activity.views import *

router = routers.DefaultRouter()

urlpatterns = [
    path('new_playlist', new_playlist, name="new_playlist"),
    path('add_song_to_playlist', add_song_to_playlist, name="add_song_to_playlist"),
    path('remove_song_from_playlist', remove_song_from_playlist, name="remove_song_from_playlist"),
    path('get_all_playlists_of_user', get_all_playlists_of_user, name="get_all_playlists_of_user"),
]
