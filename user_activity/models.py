from django.db import models


class SongLikes(models.Model):
    id = models.AutoField(primary_key=True)
    song_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250)


class SongComments(models.Model):
    id = models.AutoField(primary_key=True)
    song_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250)
    comment = models.CharField(max_length=250)


class SongListens(models.Model):
    id = models.AutoField(primary_key=True)
    song_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250)
    count = models.IntegerField(default=1)
