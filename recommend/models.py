from django.contrib.postgres.fields import ArrayField
from django.db import models

from songsapi.models import DFSong


class SongEmbedding(models.Model):
    row_number = models.IntegerField(default=-1)
    song_id = models.CharField(max_length=250, primary_key=True)
    embedding = ArrayField(models.IntegerField(default=0))


class RecommendedSong(models.Model):
    song = models.ForeignKey(DFSong, on_delete=models.CASCADE)
    recommends_songs_id = ArrayField(ArrayField(models.CharField(max_length=250)))
