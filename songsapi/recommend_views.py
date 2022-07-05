import random
from ast import literal_eval

from df.DFResponse import DFResponse
from songsapi.ArtistEdge import ArtistGraph
from songsapi.models import *

from df.utils import *
from songsapi.static_database_utils import get_df_song_by_id, get_artist
from user_activity.models import SongListens


def get_recommended_songs(request):
    result = []
    requested_song_id = request.GET.get('song_id', None)
    df_song = get_df_song_by_id(requested_song_id)
    recommended_songs_id = RecommendedSongs.objects.filter(song=df_song)
    if len(recommended_songs_id) > 0:
        for song_id in recommended_songs_id[0].recommends_songs_id:
            result.append(song_df_to_map(get_df_song_by_id(song_id)))
    return DFResponse(data=result, is_successful=True)


def get_listened_playlist(user_id):
    result = []
    song_listened_list = SongListens.objects.filter(user_id=user_id)
    count_listened = [song_listens.count for song_listens in song_listened_list]
    print("count_listened")
    if len(count_listened) >= 1:
        song_listens = set(random.choices(song_listened_list, weights=tuple(count_listened), k=10))
        print(song_listened_list)
        for song_id in song_listens:
            df_song = get_df_song_by_id(song_id.song_id.id)
            if df_song is not None:
                result.append(song_df_to_map(df_song))
    return result


def get_general_recommended_unlistened_songs(user_id):
    rec_list = set()
    song_listened_list = SongListens.objects.filter(user_id=user_id)
    count_listened = [song_listens.count for song_listens in song_listened_list]
    if len(count_listened) >= 1:
        listened_playlist = set(random.choices(song_listened_list, weights=tuple(count_listened), k=10))
        for song_listened in listened_playlist:
            df_song = get_df_song_by_id(song_listened.song_id.id)
            if df_song is None:
                continue
            else:
                rec_songs = RecommendedSongs.objects.filter(song=df_song.id)[0]
                rec_list = rec_list.union(set(random.choices(rec_songs.recommends_songs_id[1:], k=2)))
    df_songs = [song_df_to_map(get_df_song_by_id(song_id)) for song_id in rec_list]
    return df_songs


def most_played_artists(user_id):
    result = []
    most_played_artists_list = {}
    song_listened_list = SongListens.objects.filter(user_id=user_id).order_by('count')
    for song in song_listened_list[:10]:
        df_song = get_df_song_by_id(song.song_id.id)
        artist = literal_eval(df_song.artist)[0]

        if artist in most_played_artists_list:
            most_played_artists_list[artist] += 1
        else:
            most_played_artists_list[artist] = 1

    sorted_most_played_artists = list(
        dict(reversed(sorted(most_played_artists_list.items(), key=lambda item: item[1]))).keys())

    result = [get_artist(artist1) for artist1 in sorted_most_played_artists if get_artist(artist1) is not None]
    return result


def insert_artist_edges():
    graph = ArtistGraph([])
    all_songs = DFSong.objects.all()
    for index, related_songs in enumerate(
            [rec_data.recommends_songs_id for rec_data in RecommendedSongs.objects.all()]):
        print(f"{index}/{555}")
        for i in range(len(related_songs)):
            for j in range(i + 1, len(related_songs)):
                artist1 = get_artist_of_song(related_songs[i], all_songs)
                artist2 = get_artist_of_song(related_songs[j], all_songs)
                graph.add_edge(ArtistEdge(artist1=artist1, artist2=artist2, weight=1))
    for edge in graph.graph:
        if edge.weight >= 10:
            edge.save()


def get_artist_of_song(song_id, songs: [DFSong]):
    for song in songs:
        if song.id == song_id:
            return literal_eval(song.artist)[0]
    return "NoArt"
