from ast import literal_eval

from django.contrib.auth.models import User

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
        print(literal_eval(song.artist)[0])
        if str(literal_eval(song.artist)[0]).lower() == artist:
            result.append(song_df_to_map(song))
    return result


def get_artist(artist_name):
    for artist in all_artists:
        if artist.name == artist_name:
            return {"name": artist.name, "image_url": artist.image_url}
    return None


def get_user_id(username):
    user_id = -1
    users = User.objects.filter(username=username).values_list('id')
    if len(users) >= 1:
        user_id = list(users[0])[0]
    return user_id
