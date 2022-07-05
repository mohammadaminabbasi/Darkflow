import random

from df.DFResponse import DFResponse
from songsapi.models import DFSong
from songsapi.static_database_utils import get_df_song_by_id
from user_activity.models import *


def user_listen_randomly():
    user_id = 1
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
            SongListens(song_id=get_df_song_by_id(random_song_id), user_id=User.objects.filter(id=user_id)[0],
                        count=1).save()

    return DFResponse(data="", is_successful=True)
