import random

from django.shortcuts import render
import json
import os
import time

import requests
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page

from songsapi.models import SongGenre
from songsapi.models import DFSong

from df.utils import song_to_map, rjsong_to_dfsong
from radiojavanapi import Client

rj_client = Client()


@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
@cache_page(60 * 60 * 24)  # 24 hour cache
def all_popular_songs(request):
    songs = rj_client.get_popular_songs()
    print(songs)
    songs_map = []
    for rj_song in songs:
        # rj_song = rj_client.get_song_by_id(rj_song.id)
        songs_map.append(song_to_map(rj_song))
        dfsong = rjsong_to_dfsong(rj_song)
        dfsong.genre = SongGenre.pop
        insert_song(dfsong)
    return HttpResponse(json.dumps(songs_map),
                        content_type='application/json; charset=utf8')


@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
@cache_page(60 * 60 * 24)  # 24 hour cache
def traditional_popular_songs(request):
    rj_playlist_sonati_modern = rj_client.get_music_playlist_by_url(
        "https://www.radiojavan.com/playlists/playlist/mp3/f251fce10fe5")
    rj_playlist_sonati = rj_client.get_music_playlist_by_url(
        "https://www.radiojavan.com/playlists/playlist/mp3/7e6d4b8decf2")

    songs_map = []
    for rj_song in rj_playlist_sonati_modern.songs:
        rj_song = rj_client.get_song_by_id(rj_song.id)
        songs_map.append(song_to_map(rj_song))
        dfsong = rjsong_to_dfsong(rj_song)
        dfsong.genre = SongGenre.pop
        insert_song(dfsong)

    for rj_song in rj_playlist_sonati.songs:
        rj_song = rj_client.get_song_by_id(rj_song.id)
        songs_map.append(song_to_map(rj_song))
        dfsong = rjsong_to_dfsong(rj_song)
        dfsong.genre = SongGenre.pop
        insert_song(dfsong)

    return HttpResponse(json.dumps(songs_map),
                        content_type='application/json; charset=utf8')


@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
@cache_page(60 * 60 * 24)  # 24 hour cache
def pop_popular_songs(request):
    songs_map = []
    rj_playlist_pop = rj_client.get_music_playlist_by_url(
        "https://www.radiojavan.com/playlists/playlist/mp3/6449cdabd351")
    for rj_song in rj_playlist_pop.songs:
        rj_song = rj_client.get_song_by_id(rj_song.id)
        songs_map.append(song_to_map(rj_song))
        dfsong = rjsong_to_dfsong(rj_song)
        dfsong.genre = SongGenre.pop
        insert_song(dfsong)
    return HttpResponse(json.dumps(songs_map),
                        content_type='application/json; charset=utf8')


@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
@cache_page(60 * 60 * 24)  # 24 hour cache
def hiphop_popular(request):
    rj_playlist_hiphop = rj_client.get_music_playlist_by_url(
        "https://www.radiojavan.com/playlists/playlist/mp3/3ff92ab663a3")
    songs_map = []
    for rj_song in rj_playlist_hiphop.songs:
        rj_song = rj_client.get_song_by_id(rj_song.id)
        songs_map.append(song_to_map(rj_song))
        dfsong = rjsong_to_dfsong(rj_song)
        dfsong.genre = SongGenre.hiphop
        insert_song(dfsong)

    return HttpResponse(json.dumps(songs_map),
                        content_type='application/json; charset=utf8')


def insert_song(song: DFSong):
    if not DFSong.objects.filter(pk=song.id).exists():
        print(22)
        # song.save()
