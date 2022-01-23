from django.template.defaulttags import url
from django.urls import include, path, re_path
from rest_framework import routers

from recommend.views import *

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('insert/', insert_embedding_to_song_db, name="recommend_by_embedding"),
    path('update_embedding/', update_embedding, name="update_embedding"),
    re_path(r'^$', recommend_by_embedding),
]
