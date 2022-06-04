from django.urls import include, path
from rest_framework import routers

from songsapi.views import *

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('popular_songs/', all_popular_songs, name="popular_songs"),
    path('traditional_popular/', traditional_popular_songs, name="traditional_popular_songs"),
    path('pop_popular/', pop_popular_songs, name="pop_popular_songs"),
    path('hiphop_popular/', hiphop_popular, name="hiphop_popular_songs"),
    path('testing/', hiphop_popular, name="testing")
]