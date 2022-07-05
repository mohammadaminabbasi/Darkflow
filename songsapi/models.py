import enum

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django import forms
from django.conf import settings


class DFSong(models.Model):
    id = models.CharField(max_length=250, primary_key=True)
    title = models.CharField(max_length=1000)
    artist = models.CharField(max_length=1000, default="")
    songUrl = models.URLField()
    imageUrl = models.URLField()
    lyric = models.TextField(null=True)
    likes = models.IntegerField(default=0)
    genre = models.CharField(max_length=100, default="")
    tokens = models.TextField(default="")


class DFArtist(models.Model):
    name = models.CharField(primary_key=True, max_length=1000)
    image_url = models.URLField()


class RecommendedSongs(models.Model):
    song = models.OneToOneField(DFSong, on_delete=models.CASCADE, primary_key=True)
    recommends_songs_id = ArrayField(models.CharField(max_length=250))


class SongGenre(enum.Enum):
    pop = "pop"
    traditional = "traditional"


class ArtistEdge(models.Model):
    id = models.AutoField(primary_key=True)
    artist1 = models.ForeignKey(DFArtist, on_delete=models.CASCADE, related_name="artist1")
    artist2 = models.ForeignKey(DFArtist, on_delete=models.CASCADE, related_name="artist2")
    weight = models.IntegerField(default=1)
