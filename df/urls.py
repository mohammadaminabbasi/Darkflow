from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('songsapi/', include('songsapi.urls')),
    path('auth/', include('auth.urls')),
]
