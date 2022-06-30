from django.urls import include, path
from rest_framework import routers

from songsapi.recommend_views import *
from songsapi.views import *

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('popular_songs', all_popular_songs, name="popular_songs"),
    path('traditional_popular', traditional_popular_songs, name="traditional_popular_songs"),
    path('pop_popular', pop_popular_songs, name="pop_popular_songs"),
    path('artist_songs', get_songs_of_artist, name="songs"),
    path('rec_special_song', get_recommended_songs, name="get_recommended_songs"),
    path('history_playlist', get_listened_playlist, name="get_recommended_songs"),
    path('recommended_artists', most_played_artists, name="recommend_artist"),
    path('general_recommended_songs', get_general_recommended_unlistened_songs, name="recommend_artist")
]
