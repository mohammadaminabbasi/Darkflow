from django.urls import path, include
from django.contrib import admin

from df.views import home, run
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('run/', run, name="home"),
    path('songsapi/', include('songsapi.urls')),
    path('user_activity/', include('user_activity.urls')),
    path('playlist/', include('user_activity.playlist_urls')),
    path('auth/', include('auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
