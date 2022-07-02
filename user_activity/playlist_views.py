import random

from df.DFResponse import DFResponse
from df.utils import comments_to_map, song_df_to_map
from songsapi.models import *
from songsapi.static_database_utils import get_df_song_by_id, get_artist
from user_activity.models import *


def new_playlist(request):
    name = request.GET.get('name', None)
    user_id = request.GET.get('user_id', None)
    PlayList(name=name, user_id=user_id, songs_id=[]).save()
    return DFResponse(message="playlist created!", is_successful=True)


def add_song_to_playlist(request):
    song_id = request.GET.get('song_id', None)
    playlist_id = request.GET.get('playlist_id', None)
    playlist = PlayList.objects.filter(id=playlist_id)[0]
    if song_id is not None and playlist_id is not None:
        playlist.songs_id.append(song_id)
        playlist.save()
    return DFResponse(message="song added to playlist!", is_successful=True)


def remove_song_from_playlist(request):
    song_id = request.GET.get('song_id', None)
    playlist_id = request.GET.get('playlist_id', None)
    playlist = PlayList.objects.filter(id=playlist_id)[0]
    if playlist.songs_id.__contains__(song_id):
        playlist.songs_id.remove(song_id)
        playlist.save()
        return DFResponse(message="song removed", is_successful=True)
    else:
        return DFResponse(message="song not found in playlist!", is_successful=False)


def get_all_playlists_of_user(request):
    user_id = request.GET.get('user_id', None)
    result = []
    for playlist in PlayList.objects.all():
        if playlist.user_id == user_id:
            playlist_songs = []
            for song_id in playlist.songs_id:
                playlist_songs.append(song_df_to_map(get_df_song_by_id(song_id)))

            artist_images = []
            random_choices_count = 0
            if len(playlist_songs) >= 2:
                random_choices_count = 2
            elif len(playlist_songs) == 1:
                random_choices_count = 1

            for song_map in random.choices(playlist_songs, k=random_choices_count):
                artist_images.append(get_artist(song_map["artist"][0])["image_url"])

            playlist_map = {"id": playlist.id,
                            "name": playlist.name,
                            "songs": playlist_songs,
                            "artist_images": list(set(artist_images))}
            result.append(playlist_map)
    return DFResponse(data=result, is_successful=True)
