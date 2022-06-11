from radiojavanapi import Client
from radiojavanapi.models import Song, Artist

from songsapi.models import *
from finglish import f2p

from user_activity.models import *


def rjsong_to_dfsong(song: Song):
    dfsong = DFSong()
    dfsong.id = song.id
    dfsong.title = song.name
    dfsong.artist = song.artist
    dfsong.songUrl = song.link
    dfsong.imageUrl = song.photo
    dfsong.lyric = song.lyric
    return dfsong


def rjartist_to_dfartist(artist: Artist):
    dfartist = DFArtist()
    dfartist.name = artist.name
    dfartist.imageUrl = artist.photo
    return dfartist


def rjsong_to_map(song: Song):
    song_map = {
        "id": str(song.id),
        "title": str(convert_finglish_to_persian(song.name)),
        "artist": str(convert_finglish_to_persian(song.artist)),
        "songUrl": str(song.link),
        "imageUrl": str(song.photo),
    }
    return song_map


def song_df_to_map(song: DFSong):
    song_map = {
        "id": str(song.id),
        "title": str(convert_finglish_to_persian(song.title)),
        "artist": str(convert_finglish_to_persian(song.artist)),
        "songUrl": str(song.songUrl),
        "imageUrl": str(song.imageUrl),
    }
    return song_map


def artist_to_map(artist: DFArtist):
    song_map = {
        "en_name": str(artist.name),
        "fa_name": str(convert_finglish_to_persian(artist.name)),
        "imageUrl": str(artist.imageUrl),
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


def convert_finglish_to_persian(finglish: str):
    persian = f2p(finglish).replace("فت ", "فیت ")
    return persian
