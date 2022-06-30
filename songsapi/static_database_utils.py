from ast import literal_eval

from df.utils import song_df_to_map
from songsapi.models import DFSong, DFArtist

all_songs = DFSong.objects.all()
all_artists = DFArtist.objects.all()


def get_df_song_by_id(song_id):
    for song in all_songs:
        if song.id == song_id:
            return song
    return None


def get_df_songs_of_artist(artist):
    result = []
    for song in all_songs:
        if literal_eval(song.artist)[0]:
            result.append(song_df_to_map(song))
    return result


def get_artist(artist_name):
    for artist in all_artists:
        if artist.name == artist_name:
            return {"name": artist.name, "image_url": artist.image_url}
    return None
