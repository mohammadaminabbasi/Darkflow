from df.DFResponse import DFResponse
from df.utils import comments_to_map, song_df_to_map
from songsapi.models import *
from songsapi.static_database_utils import get_df_song_by_id, get_user_id
from user_activity.models import *


def like_song(request):
    song_id = request.GET.get('song_id', None)
    user_id = get_user_id(request.GET.get('user_id', None))
    if user_id != -1:
        if not SongLikes.objects.filter(song_id=song_id, user_id=user_id).exists():
            if DFSong.objects.filter(id=song_id).exists():
                SongLikes(song_id=DFSong.objects.filter(id=song_id)[0],
                          user_id=User.objects.filter(id=user_id)[0]).save()
                return DFResponse(message="song liked!", is_successful=True)
    return DFResponse(message="Error!", is_successful=False)


def unlike_song(request):
    song_id = request.GET.get('song_id', None)
    user_id = get_user_id(request.GET.get('user_id', None))
    if SongLikes.objects.filter(song_id=song_id, user_id=user_id).exists():
        SongLikes.objects.filter(song_id=song_id, user_id=user_id)[0].delete()
        return DFResponse(message="song unliked!", is_successful=True)
    return DFResponse(message="song not unliked!", is_successful=True)


def is_song_liked_by_user(request):
    song_id = request.GET.get('song_id', None)
    user_id = get_user_id(request.GET.get('user_id', None))
    if SongLikes.objects.filter(song_id=song_id, user_id=user_id).exists():
        return DFResponse(data=True, message="song unliked!", is_successful=True)
    else:
        return DFResponse(data=False, message="song unliked!", is_successful=True)


def comment_song(request):
    song_id = request.GET.get('song_id', None)
    user_id = get_user_id(request.GET.get('user_id', None))
    comment = request.GET.get('comment', None)
    if user_id != -1 and DFSong.objects.filter(id=song_id).exists():
        SongComments(song_id=DFSong.objects.filter(id=song_id)[0],
                     user_id=User.objects.filter(id=user_id)[0],
                     comment=comment).save()
        return DFResponse(message="comment submitted!1111", is_successful=True)
    else:
        return DFResponse(message="Error", is_successful=False)


def get_all_song_comments(request):
    song_id = request.GET.get('song_id', None)
    if DFSong.objects.filter(id=song_id).exists():
        comments = SongComments.objects.filter(song_id=song_id)
        return DFResponse(data=comments_to_map(comments), is_successful=True)
    else:
        return DFResponse(message="Error", is_successful=False)


def add_new_song_listen(request):
    song_id = request.GET.get('song_id', None)
    user_id = get_user_id(request.GET.get('user_id', None))
    print(type(request))
    if SongListens.objects.filter(song_id=song_id, user_id=user_id).exists():
        song_listen = SongListens.objects.filter(song_id=song_id, user_id=user_id)[0]
        song_listen.count = song_listen.count + 1
        song_listen.save()
        return DFResponse(message="Song Listens submitted", is_successful=True)
    else:
        if DFSong.objects.filter(id=song_id).exists() and user_id != -1:
            SongListens(song_id=DFSong.objects.filter(id=song_id)[0],
                        user_id=User.objects.filter(id=user_id)[0],
                        count=1).save()
            return DFResponse(message="Song Listens submitted", is_successful=True)

    return DFResponse(message="Error", is_successful=False)


def get_all_liked_songs_by_user(request):
    result = []
    user_id = get_user_id(request.GET.get('user_id', None))
    if SongLikes.objects.filter(user_id=user_id).exists():
        for song_Like in SongLikes.objects.filter(user_id=user_id):
            print(song_Like.song_id)
            result.append(song_df_to_map(get_df_song_by_id(song_Like.song_id.id)))
    return DFResponse(data=result, message="", is_successful=True)
