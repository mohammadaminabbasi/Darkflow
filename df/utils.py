import re
from ast import literal_eval

from radiojavanapi.models import Song, Artist

from songsapi.models import *

from user_activity.models import *


def rjsong_to_dfsong(song: Song):
    dfsong = DFSong()
    dfsong.id = song.id
    dfsong.title = re.sub(r'\([^()]*\)', '', song.name)
    dfsong.artist = str(song.artist_tags)
    print(str(dfsong.artist))
    dfsong.songUrl = song.link
    dfsong.likes = song.likes
    dfsong.imageUrl = song.photo
    dfsong.lyric = song.lyric
    return dfsong


def rjartist_to_dfartist(artist: Artist):
    dfartist = DFArtist()
    dfartist.name = artist.name
    dfartist.image_url = artist.photo
    return dfartist


def song_rj_to_map(song: Song):
    song_map = {
        "id": str(song.id),
        "title": str(song.name),
        "artist": str(song.artist),
        "songUrl": str(song.link),
        "imageUrl": str(song.photo),
    }
    return song_map


def song_df_to_map(song: DFSong):
    song_map = {
        "id": str(song.id),
        "title": str(song.title),
        "artist": literal_eval(song.artist),
        "songUrl": str(song.songUrl),
        "imageUrl": str(song.imageUrl),
    }
    return song_map


def artist_to_map(artist: DFArtist):
    song_map = {
        "en_name": str(artist.name),
        "fa_name": str(artist.name),
        "imageUrl": str(artist.image_url),
    }
    return song_map


def comments_to_map(comments: [SongComments]):
    maps = []
    for comment in comments:
        map = {
            "id": str(comment.id),
            "song_id": str(comment.song_id),
            "user_id": str(comment.user_id),
            "comment": str(comment.comment),
        }
        maps.append(map)
    return maps


def song_listens_to_map(song_listens: [SongListens]):
    maps = []
    for song_listen in song_listens:
        map = {
            "id": str(song_listen.id),
            "song_id": str(song_listen.song_id),
            "user_id": str(song_listen.user_id),
            "count": str(song_listen.count),
        }
        maps.append(map)
    return maps
