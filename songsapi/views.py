from os import environ

import requests
from django.contrib.sites.models import Site
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest
from radiojavanapi import Client
from rest_framework import request
from rest_framework.decorators import permission_classes, api_view
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated

from df.DFResponse import DFResponse
from tools.StopWords import StopWords
from songsapi.models import *

from df.utils import *

rj_client = Client()


@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
@cache_page(60 * 60 * 24)  # 24 hour cache
def all_popular_songs(request):
    print("all_popular_songs")
    songs = rj_client.get_popular_songs()
    print("rj_client.get_popular_songs")
    songs_map = []
    for rj_song in songs:
        songs_map.append(rjsong_to_map(rj_song))
        dfsong = rjsong_to_dfsong(rj_song)
        insert_song(dfsong)
    return DFResponse(data=songs_map, is_successful=True)


@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
@cache_page(60 * 60 * 24)  # 24 hour cache
def traditional_popular_songs(request):
    rj_playlist_sonati_modern = rj_client.get_music_playlist_by_url(
        "https://www.radiojavan.com/playlists/playlist/mp3/f251fce10fe5")
    rj_playlist_sonati = rj_client.get_music_playlist_by_url(
        "https://www.radiojavan.com/playlists/playlist/mp3/7e6d4b8decf2")

    songs_map = []
    for rj_song in rj_playlist_sonati_modern.songs:
        songs_map.append(rjsong_to_map(rj_song))
        dfsong = rjsong_to_dfsong(rj_song)
        dfsong.genre = SongGenre.traditional
        insert_song(dfsong)

    for rj_song in rj_playlist_sonati.songs:
        songs_map.append(rjsong_to_map(rj_song))
        dfsong = rjsong_to_dfsong(rj_song)
        dfsong.genre = SongGenre.traditional
        insert_song(dfsong)

    return DFResponse(data=songs_map, is_successful=True)


# @api_view(['GET'])
# @permission_classes((IsAuthenticated,))
@cache_page(60 * 60 * 24)  # 24 hour cache
def pop_popular_songs(request):
    songs_map = []
    rj_playlist_pop = rj_client.get_music_playlist_by_url(
        "https://www.radiojavan.com/playlists/playlist/mp3/6449cdabd351")
    for rj_song in rj_playlist_pop.songs:
        songs_map.append(rjsong_to_map(rj_song))
        dfsong = rjsong_to_dfsong(rj_song)
        dfsong.genre = SongGenre.pop
        insert_song(dfsong)
    return DFResponse(data=songs_map, is_successful=True)


@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
@cache_page(60 * 60 * 24)  # 24 hour cache
def hiphop_popular(request):
    rj_playlist_hiphop = rj_client.get_music_playlist_by_url(
        "https://www.radiojavan.com/playlists/playlist/mp3/3ff92ab663a3")
    songs_map = []
    for rj_song in rj_playlist_hiphop.songs:
        songs_map.append(rjsong_to_map(rj_song))
        dfsong = rjsong_to_dfsong(rj_song)
        dfsong.genre = SongGenre.hiphop
        insert_song(dfsong)

    return DFResponse(data=songs_map, is_successful=True)


@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
# @cache_page(60 * 60 * 24)  # 24 hour cache
def related_artist(request):
    popular_artists = rj_client.get_popular_artists()[0:10]
    artists_map = []
    for artist in popular_artists:
        dfartist = rjartist_to_dfartist(artist)
        artists_map.append(artist_to_map(dfartist))

    return DFResponse(data=artists_map, is_successful=True)


def get_songs_of_artist(request):
    artist = request.GET.get('artist', None)
    print(artist)
    rj_artist = rj_client.get_artist_by_name(artist)
    songs_map = []
    for song in rj_artist.songs[0:10]:
        songs_map.append(rjsong_to_map(rj_client.get_song_by_id(song.id)))

    return DFResponse(data=songs_map, is_successful=True)


def like_song(request):
    song_id = request.GET.get('song_id', None)
    user_id = request.GET.get('user_id', None)
    if not SongLikes.objects.filter(song_id=song_id, user_id=user_id).exists():
        SongLikes(song_id=song_id, user_id=user_id).save()
    return DFResponse(message="song liked!", is_successful=True)


def unlike_song(request):
    song_id = request.GET.get('song_id', None)
    user_id = request.GET.get('user_id', None)
    if SongLikes.objects.filter(song_id=song_id, user_id=user_id).exists():
        SongLikes.objects.filter(song_id=song_id, user_id=user_id)[0].delete()
        return DFResponse(message="song unliked!", is_successful=True)
    return DFResponse(message="song not liked!", is_successful=True)


def comment_song(request):
    song_id = request.GET.get('song_id', None)
    user_id = request.GET.get('user_id', None)
    comment = request.GET.get('comment', None)
    SongComments(song_id=song_id, user_id=user_id, comment=comment).save()
    return DFResponse(message="comment submitted!1111", is_successful=True)


def insert_song(song: DFSong):
    stop_words = StopWords()
    if not DFSong.objects.filter(pk=song.id).exists():
        song.lyric = stop_words.remove_stop_words_of_sentences(song.lyric if song.lyric is not None else "")
        song.save()
