from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include, re_path
from rest_framework import routers

from df.views import *
from df.views import index_req

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('songsapi/', include('songsapi.urls')),
    path('recommender/', include('recommend.urls')),
    path('auth/', include('auth.urls')),
    path('ping1', ping1, name="ping"),
    re_path(r'^page/$', index_req),
]
