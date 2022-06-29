from songsapi.models import DFSong

all_songs = DFSong.objects.all()


def get_df_song_by_id(song_id):
    for song in all_songs:
        if song.id == song_id:
            return song
    return None
