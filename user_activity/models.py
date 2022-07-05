from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

from songsapi.models import DFSong


class SongLikes(models.Model):
    id = models.AutoField(primary_key=True)
    song_id = models.ForeignKey(DFSong, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class SongComments(models.Model):
    id = models.AutoField(primary_key=True)
    song_id = models.ForeignKey(DFSong, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)


class SongListens(models.Model):
    id = models.AutoField(primary_key=True)
    song_id = models.ForeignKey(DFSong, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)


class PlayList(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250,default="")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    songs_id = ArrayField(models.CharField(max_length=250))
