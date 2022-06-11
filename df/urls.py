from django.urls import path, include
from django.contrib import admin

from df.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('songsapi/', include('songsapi.urls')),
    path('user_activity/', include('user_activity.urls')),
    path('auth/', include('auth.urls')),
]
