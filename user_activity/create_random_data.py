import random

from df.DFResponse import DFResponse
from songsapi.models import DFSong
from user_activity.models import *


def user_listen_randomly():
    user_id = "koalamin"
    songs = DFSong.objects.all()
    for i in range(50):
        print(i)
        random_song_id = random.choice(songs).id
        print(random_song_id)
        if SongListens.objects.filter(song_id=random_song_id, user_id=user_id).exists():
            song_listen = SongListens.objects.filter(song_id=random_song_id, user_id=user_id)[0]
            song_listen.count = song_listen.count + 1
            song_listen.save()
        else:
            SongListens(song_id=random_song_id, user_id=user_id, count=1).save()

    return DFResponse(data="", is_successful=True)
