from django.contrib import admin

from recommend.models import SongEmbedding, RecommendedSong
from songsapi.models import DFSong

admin.site.register(DFSong)
admin.site.register(SongEmbedding)
admin.site.register(RecommendedSong)
