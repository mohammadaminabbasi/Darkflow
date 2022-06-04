import enum

from django.db import models
from django.contrib.postgres.fields import ArrayField


class DFSong(models.Model):
    id = models.CharField(max_length=250, primary_key=True)
    title = models.CharField(max_length=1000)
    artist = models.CharField(max_length=1000, default="")
    songUrl = models.URLField()
    imageUrl = models.URLField()
    lyric = models.TextField(null=True)
    # likes = models.IntegerField(default=0)
    genre = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.title


class SongLikes(models.Model):
    id = models.AutoField(primary_key=True)
    song_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250)


class SongComments(models.Model):
    id = models.AutoField(primary_key=True)
    song_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250)
    comment = models.CharField(max_length=250)


class DFArtist(models.Model):
    name = models.CharField(primary_key=True, max_length=1000)
    imageUrl = models.URLField()

    def __str__(self):
        return self.name


class RecommendedSongs(models.Model):
    song = models.ForeignKey(DFSong, on_delete=models.CASCADE, primary_key=True, unique=True)
    recommends_songs_id = ArrayField(models.CharField(max_length=250))


class SongGenre(enum.Enum):
    hiphop = "hiphop"
    pop = "pop"
    traditional = "traditional"
