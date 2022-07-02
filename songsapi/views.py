from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view

from df.DFResponse import DFResponse
from songsapi.recommend_views import get_general_recommended_unlistened_songs, most_played_artists, \
    get_listened_playlist
from songsapi.static_database_utils import get_df_songs_of_artist
from songsapi.translate_utlis import *

from df.utils import *

rj_client = Client()
is_online_mode = False


def all_popular_songs():
    result_map_list = []

    if is_online_mode:

        songs = rj_client.get_popular_songs()
        for rj_song in songs:
            result_map_list.append(song_rj_to_map(rj_song))

    else:

        songs = DFSong.objects.order_by('-likes')[0:10]
        for song in songs:
            result_map_list.append(song_df_to_map(song))

    return result_map_list


def traditional_popular_songs():
    result_map_list = []

    if is_online_mode:
        rj_playlist_sonati_modern = rj_client.get_music_playlist_by_url(
            "https://www.radiojavan.com/playlists/playlist/mp3/f251fce10fe5")
        rj_playlist_sonati = rj_client.get_music_playlist_by_url(
            "https://www.radiojavan.com/playlists/playlist/mp3/7e6d4b8decf2")

        for rj_song in rj_playlist_sonati_modern.songs + rj_playlist_sonati.songs:
            result_map_list.append(song_rj_to_map(rj_song))

    else:
        songs = DFSong.objects.filter(genre=SongGenre.traditional
                                      ).order_by('-likes')[0:10]
        for song in songs:
            result_map_list.append(song_df_to_map(song))

    return result_map_list


def pop_popular_songs(request):
    result_map_list = []

    if is_online_mode:
        rj_playlist_pop = rj_client.get_music_playlist_by_url(
            "https://www.radiojavan.com/playlists/playlist/mp3/6449cdabd351")
        for rj_song in rj_playlist_pop.songs:
            result_map_list.append(song_rj_to_map(rj_song))

    else:
        songs = DFSong.objects.filter(genre=SongGenre.pop
                                      ).order_by('-likes')[0:10]
        for song in songs:
            result_map_list.append(song_df_to_map(song))

    return DFResponse(data=result_map_list, is_successful=True)


def get_songs_of_artist(request):
    artist = request.GET.get('artist', None)
    print("get_songs_of_artist")
    print(artist)
    result = get_df_songs_of_artist(artist)
    print(result)
    return DFResponse(data=result, is_successful=True)


@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
@cache_page(60 * 60 * 24)  # 24 hour cache
def get_all_home_page_data(request):
    user_id = request.GET.get('user_id', None)
    result = []
    popular_songs = all_popular_songs()
    result.append({"type": "song", "name": translate_popular_songs, "songs": popular_songs})
    recommended_artists = most_played_artists(user_id)
    result.append({"type": "artist", "name": translate_rec_artists, "artists": recommended_artists})
    recommended_songs = get_general_recommended_unlistened_songs(user_id)
    result.append({"type": "song", "name": translate_rec_songs, "songs": recommended_songs})
    traditional_songs = traditional_popular_songs()
    result.append({"type": "song", "name": translate_traditional_popular_songs, "songs": traditional_songs})
    history_playlist = get_listened_playlist(user_id)
    result.append({"type": "song", "name": translate_history_playlist, "songs": history_playlist})
    return DFResponse(data=result, is_successful=True)
