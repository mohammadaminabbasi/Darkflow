from radiojavanapi.models import Song

from songsapi.models import DFSong


def song_to_map(song: Song):
    song_map = {
        "id": str(song.id),
        "title": str(song.name),
        "artist": str(song.artist),
        "songUrl": str(song.link),
        "imageUrl": str(song.photo),
    }
    return song_map


def rjsong_to_dfsong(song: Song):
    dfsong = DFSong()
    dfsong.id = song.id
    dfsong.title = song.name
    dfsong.artist = song.artist
    dfsong.songUrl = song.link
    dfsong.imageUrl = song.photo
    dfsong.lyric = song.lyric
    return dfsong


def song_df_to_map(song: DFSong):
    song_map = {
        "id": str(song.id),
        "title": str(song.title),
        "artist": str(song.artist),
        "songUrl": str(song.songUrl),
        "imageUrl": str(song.imageUrl),
    }
    return song_map
