from df.DFResponse import DFResponse
from songsapi.models import *

from df.utils import song_df_to_map
from songsapi.views import all_popular_songs


def get_recommended_songs(request):
    song_id = request.GET.get('song_id', None)
    if song_id is None:
        all_popular_songs(request)
    import logging
    logger = logging.getLogger('testlogger')
    logger.info("song_id")
    logger.info(song_id)
    print("song_id")
    print(song_id)
    if song_id is not None:
        suggested_songs_map = []
        if RecommendedSongs.objects.filter(song_id=song_id).exists():
            recommended_songs = RecommendedSongs.objects.get(song_id=song_id)
            print(str(recommended_songs.recommends_songs_id).strip("{}").split(","))
            for recommended_song_id in str(recommended_songs.recommends_songs_id).strip("{}").split(","):
                if DFSong.objects.filter(id=recommended_song_id).exists():
                    df_song = DFSong.objects.get(id=recommended_song_id)
                    suggested_songs_map.append(song_df_to_map(df_song))
                else:
                    return all_popular_songs(request)
                    # return DFResponse(message="No song in db", is_successful=False)

            return DFResponse(data=suggested_songs_map, is_successful=True)
        else:
            return all_popular_songs(request)
            # return DFResponse(message="No Recommends for this song", is_successful=False)
    else:
        return all_popular_songs(request)
        # return DFResponse(message="ID of song in null", is_successful=False)


def init_rec_date(request):
    from recommend.views import update_embedding_db
    from recommend.views import insert_recommended_songs_for_each_song
    update_embedding_db()
    insert_recommended_songs_for_each_song()
