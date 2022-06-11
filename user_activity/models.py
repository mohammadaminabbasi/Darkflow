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
    likes = models.IntegerField(default=0)
    genre = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.title
