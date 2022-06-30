import json
import random
from ast import literal_eval

import hazm
import numpy as np

from df.DFResponse import DFResponse
from songsapi.ArtistEdge import ArtistEdge, Graph
from songsapi.models import *

from df.utils import song_df_to_map, song_listens_to_map
from songsapi.static_database_utils import get_df_song_by_id
from songsapi.views import all_popular_songs
from user_activity.models import SongListens


def get_recommended_songs(request):
    result = []
    requested_song_id = request.GET.get('song_id', None)
    df_song = get_df_song_by_id(requested_song_id)
    recommended_songs_id = RecommendedSongs.objects.filter(song=df_song)
    if len(recommended_songs_id) > 0:
        for song_id in recommended_songs_id[0].recommends_songs_id:
            result.append(song_df_to_map(get_df_song_by_id(song_id)))
    else:
        return all_popular_songs(request)
    return DFResponse(data=result, is_successful=True)


def get_listened_playlist(request):
    result = []
    user_id = request.GET.get('user_id', None)
    song_listened_list = SongListens.objects.filter(user_id=user_id)
    count_listened = [song_listens.count for song_listens in song_listened_list]
    song_listens = set(random.choices(song_listened_list, weights=tuple(count_listened), k=10))
    for song_id in song_listens:
        print(song_id.song_id)
        df_song = get_df_song_by_id(song_id.song_id)
        if df_song is not None:
            result.append(song_df_to_map(df_song))
    return DFResponse(data=result, is_successful=True)


def get_general_recommended_unlistened_songs(request):
    rec_list = set()
    user_id = request.GET.get('user_id', None)
    song_listened_list = SongListens.objects.filter(user_id=user_id)
    count_listened = [song_listens.count for song_listens in song_listened_list]
    listened_playlist = set(random.choices(song_listened_list, weights=tuple(count_listened), k=10))
    print(listened_playlist)
    for song_listened in listened_playlist:
        print(song_listened.song_id)
        df_song = get_df_song_by_id(song_listened.song_id)
        rec_songs = RecommendedSongs.objects.filter(song=df_song)[0]
        rec_list = rec_list.union(set(random.choices(rec_songs.recommends_songs_id[1:], k=2)))
    df_songs = [song_df_to_map(get_df_song_by_id(song_id)) for song_id in rec_list]
    return DFResponse(data=df_songs, is_successful=True)


def most_played_artists(request):
    user_id = request.GET.get('user_id', None)
    most_played_artists_list = {}
    song_listened_list = SongListens.objects.filter(user_id=user_id).order_by('count')
    for song in song_listened_list[:5]:
        df_song = get_df_song_by_id(song.song_id)
        artist = literal_eval(df_song.artist)[0]
        print(artist)

        if artist in most_played_artists_list:
            most_played_artists_list[artist] += 1
        else:
            most_played_artists_list[artist] = 1

    print(most_played_artists_list)
    sorted_most_played_artists = dict(reversed(sorted(most_played_artists_list.items(), key=lambda item: item[1])))
    print(list(sorted_most_played_artists.keys()))
    return DFResponse(data=list(sorted_most_played_artists.keys()), is_successful=False)


def insert_artist_edges():
    graph = Graph([])
    all_songs = DFSong.objects.all()
    print(len([rec_data.recommends_songs_id for rec_data in RecommendedSongs.objects.all()]))
    for index, related_songs in enumerate(
            [rec_data.recommends_songs_id for rec_data in RecommendedSongs.objects.all()]):
        print(f"{index}/{555}")
        for i in range(len(related_songs)):
            for j in range(i + 1, len(related_songs)):
                artist1 = get_artist_of_song(related_songs[i], all_songs)
                artist2 = get_artist_of_song(related_songs[j], all_songs)
                graph.add_edge(ArtistEdge(artist1=artist1, artist2=artist2, weight=1))
    for edge in graph.graph:
        print(edge)
        if edge.weight >= 10:
            edge.save()


def get_artist_of_song(song_id, songs: [DFSong]):
    for song in songs:
        if song.id == song_id:
            return literal_eval(song.artist)[0]
    return "NoArt"
