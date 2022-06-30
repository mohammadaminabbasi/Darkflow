from django.urls import include, path
from rest_framework import routers

from songsapi.recommend_views import *
from songsapi.views import *

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('home_page_data', get_all_home_page_data, name="home_page_data"),
    path('artist_songs', get_songs_of_artist, name="songs"),
    path('rec_special_song', get_recommended_songs, name="get_recommended_songs"),
]
