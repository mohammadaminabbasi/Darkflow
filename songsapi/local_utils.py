import glob, os
from ast import literal_eval

from radiojavanapi import Client

from df.DFResponse import DFResponse
from df.utils import rjsong_to_dfsong
from songsapi.models import SongGenre, DFSong, DFArtist
from songsapi.static_database_utils import all_songs


def import_pop_music_to_database():
    print("import_pop_music_to_database")
    client = Client()
    root_path = "/home/koalamin/1.Programming/3.NLP/SimpleChatBot/"
    os.chdir("/home/koalamin/1.Programming/3.NLP/SimpleChatBot/sonati")
    mp3_files = [root_path + path for path in glob.glob("*.mp3")]
    os.chdir("/home/koalamin/1.Programming/3.NLP/SimpleChatBot/pop")
    mp3_files = mp3_files + [root_path + path for path in glob.glob("*.mp3")]

    for i, file in enumerate(mp3_files):
        print(f"{i}/{len(mp3_files)}")
        song_id = file.replace(".mp3", "")
        print(song_id)
        if not DFSong.objects.filter(pk=song_id).exists():
            rj_song = client.get_song_by_id(file.replace(".mp3", ""))
            df_song = rjsong_to_dfsong(rj_song)
            # df_song.genre = SongGenre.pop
            print(file)

    return DFResponse(data="", is_successful=True)


def import_artists_to_db():
    client = Client()
    for i, song in enumerate(all_songs):
        print(f"{i}/{len(all_songs)}")
        for artist in literal_eval(song.artist):
            if not DFArtist.objects.filter(name=artist).exists():
                rj_artist = client.get_artist_by_name(artist)
                DFArtist(name=artist, imageUrl=rj_artist.photo).save()
