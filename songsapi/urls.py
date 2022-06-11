from django.urls import include, path
from rest_framework import routers

from songsapi.recommend_views import *
from songsapi.views import *

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('popular_songs/', all_popular_songs, name="popular_songs"),
    path('traditional_popular/', traditional_popular_songs, name="traditional_popular_songs"),
    path('pop_popular/', pop_popular_songs, name="pop_popular_songs"),
    path('hiphop_popular/', hiphop_popular, name="hiphop_popular_songs"),
    path('related_artists/', related_artist, name="related_artists"),
    path('songs/', get_songs_of_artist, name="songs"),
    path('get_recommended_songs/', get_recommended_songs, name="get_recommended_songs"),
    path('init_data/', init_rec_date, name="init_rec_date"),
]
