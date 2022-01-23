import itertools
import json

from radiojavanapi import Client
from requests import Response

from df.utils import rjsong_to_dfsong, song_df_to_map
from recommend.RecMusicByAudio import RecMusicByAudio

from django.http import JsonResponse, HttpResponse

from recommend.RecommenderByLyric import RecommenderNLP
from songsapi.models import DFSong
from recommend.models import SongEmbedding, RecommendedSong
from os import listdir
from os.path import isfile, join

from df.utils import rjsong_to_dfsong


def req(request):
    price_lte = request.GET['price_lte']
    print(price_lte)
    return JsonResponse({"2", "33"})


def recommend_by_embedding(request):
    song_id = request.GET.get('id', '53398')
    print(song_id)
    suggested_songs_map = []
    suggested_songs_df = []
    suggested_row_numbers = RecMusicByAudio().recommend_by_embedding(str(song_id))
    for suggested_song in suggested_row_numbers:
        song_embedding = SongEmbedding.objects.get(row_number=suggested_song)
        song = DFSong.objects.get(pk=song_embedding.song_id)
        suggested_songs_df.append(song)
    for song in calculate_distance_lyrical(suggested_songs_df):
        suggested_songs_map.append(song_df_to_map(song))
    return HttpResponse(json.dumps(suggested_songs_map),
                        content_type='application/json; charset=utf8')


def update_embedding(req):
    for song in DFSong.objects.all():
        if not SongEmbedding.objects.all().filter(pk=song.id).exists():
            suggested_row_numbers = RecMusicByAudio().recommend_by_embedding(str(song.id))
    return JsonResponse({"3": "2"})


def calculate_distance_lyrical(suggested_songs_df: [DFSong]):
    distance_maps = []
    print(suggested_songs_df)
    recommender_nlp = RecommenderNLP()
    for suggested_song_df in suggested_songs_df:
        if suggested_song_df.lyric is not None and suggested_songs_df[0].lyric is not None:
            distance_two_lyrics = recommender_nlp.distance_two_lyric_statics(suggested_songs_df[0].lyric,
                                                                             suggested_song_df.lyric)
            distance_map = {"song": suggested_song_df, "distance": distance_two_lyrics}
            distance_maps.append(distance_map)
        else:
            distance_map = {"song": suggested_song_df, "distance": 100}
            distance_maps.append(distance_map)
    print("distance_maps")
    print(distance_maps)
    sorted_distance_maps = sorted(distance_maps, key=lambda d: d["distance"])
    sorted_songs = [d["song"] for d in sorted_distance_maps]
    return sorted_songs


def insert_embeddings_from_local():
    path = "/home/koalamin/1.Programming/df/embedding/AllJson/"
    jsons = [f for f in listdir(path) if isfile(join(path, f))]
    for json_file_name in jsons:
        f = open(path + json_file_name)
        json_file = json.load(f)
        current_embedding = json_file['embedding']
        merged_embedding = list(itertools.chain(*current_embedding))
        song_embedding = SongEmbedding(SongEmbedding.objects.count(), str(json_file_name).replace(".json", ""),
                                       merged_embedding)
        song_embedding.save()


def insert_embedding_to_song_db(request):
    rj_client = Client()
    song_embeddings = SongEmbedding.objects.all()
    for song_embedding in song_embeddings:
        if not DFSong.objects.all().filter(pk=song_embedding.song_id).exists():
            print("not wxits")
            rj_song = rj_client.get_song_by_id(song_embedding.song_id)
            dfsong = rjsong_to_dfsong(rj_song)
            dfsong.save()

    return JsonResponse({"rec": "list"})


def update_recommended_songs(request):
    for song in SongEmbedding.objects.all():
        song_id = song.song_id
        print(song_id)
        suggested_songs_id = []
        suggested_row_numbers = RecMusicByAudio().recommend_by_embedding(str(song_id))
        for suggested_song in suggested_row_numbers:
            song_embedding = SongEmbedding.objects.get(row_number=suggested_song)
            df_song = DFSong.objects.get(pk=song_embedding.song_id)
            suggested_songs_id.append(df_song)
        RecommendedSong(song, suggested_songs_id)
    return JsonResponse({"rec": "list"})
