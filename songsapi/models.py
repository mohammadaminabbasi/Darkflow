import enum

from django.db import models


class DFSong(models.Model):
    id = models.CharField(max_length=250, primary_key=True)
    title = models.CharField(max_length=1000)
    artist = models.CharField(max_length=1000, default="")
    songUrl = models.URLField()
    imageUrl = models.URLField()
    lyric = models.TextField(null=True)
    likes = models.IntegerField(default=0)
    genre = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.title


class UserListenSong(models.Model):
    usid = models.CharField(max_length=250, primary_key=True)
    song_id = models.CharField(max_length=250)
    artist = models.CharField(max_length=250, default="")
    user_id = models.CharField(max_length=1000)

    def __str__(self):
        return self.song_id


class SongGenre(enum.Enum):
    hiphop = "hiphop"
    pop = "pop"
    traditional = "traditional"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    song_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=1000)
    Comment = models.TextField()

    def __str__(self):
        return self.Comment
