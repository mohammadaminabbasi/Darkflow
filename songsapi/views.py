from rest_framework.decorators import permission_classes, api_view
from django.views.decorators.cache import cache_page

from df.DFResponse import DFResponse
from songsapi.static_database_utils import get_df_songs_of_artist
from tools.StopWords import StopWords

from df.utils import *

rj_client = Client()
is_online_mode = False


@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
@cache_page(60 * 60 * 24)  # 24 hour cache
def all_popular_songs(request):
    result_map_list = []

    if is_online_mode:

        songs = rj_client.get_popular_songs()
        for rj_song in songs:
            result_map_list.append(song_rj_to_map(rj_song))

    else:

        songs = DFSong.objects.order_by('-likes')[0:10]
        for song in songs:
            result_map_list.append(song_df_to_map(song))

    return DFResponse(data=result_map_list, is_successful=True)


@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
@cache_page(60 * 60 * 24)  # 24 hour cache
def traditional_popular_songs(request):
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

    return DFResponse(data=result_map_list, is_successful=True)


@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
@cache_page(60 * 60 * 24)  # 24 hour cache
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
    result = get_df_songs_of_artist(artist)
    return DFResponse(data=result, is_successful=True)


def insert_song(song: DFSong):
    stop_words = StopWords()
    if not DFSong.objects.filter(pk=song.id).exists():
        song.lyric = stop_words.remove_stop_words_of_sentences(song.lyric if song.lyric is not None else "")
        song.save()
