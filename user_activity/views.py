from df.DFResponse import DFResponse
from df.utils import comments_to_map
from songsapi.models import *
from user_activity.models import *


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


def is_song_liked_by_user(request):
    song_id = request.GET.get('song_id', None)
    user_id = request.GET.get('user_id', None)
    if SongLikes.objects.filter(song_id=song_id, user_id=user_id).exists():
        return DFResponse(data=True, message="song unliked!", is_successful=True)
    else:
        return DFResponse(data=False, message="song unliked!", is_successful=True)


def comment_song(request):
    song_id = request.GET.get('song_id', None)
    user_id = request.GET.get('user_id', None)
    comment = request.GET.get('comment', None)
    SongComments(song_id=song_id, user_id=user_id, comment=comment).save()
    return DFResponse(message="comment submitted!1111", is_successful=True)


def get_all_song_comments(request):
    song_id = request.GET.get('song_id', None)
    comments = SongComments.objects.filter(song_id=song_id)
    return DFResponse(data=comments_to_map(comments), is_successful=True)


def add_new_song_listen(request):
    song_id = request.GET.get('song_id', None)
    user_id = request.GET.get('user_id', None)
    print(type(request))
    if SongListens.objects.filter(song_id=song_id, user_id=user_id).exists():
        song_listen = SongListens.objects.filter(song_id=song_id, user_id=user_id)[0]
        song_listen.count = song_listen.count + 1
        song_listen.save()
    else:
        SongListens(song_id=song_id, user_id=user_id, count=0).save()
    return DFResponse(message="Song Listens submitted", is_successful=True)


def most_listened_artists(request):
    result_map_list = {}
    for song_listen_record in SongListens.objects.all():
        artist = DFSong.objects.filter(id=song_listen_record.song_id).get().artist \
            .replace("[", "").replace("]", "").replace("'", "")

        if artist in result_map_list:
            result_map_list[artist] = result_map_list[artist] + 1
        else:
            result_map_list[artist] = 1

    return DFResponse(data=result_map_list, message="Song Listens submitted", is_successful=True)

