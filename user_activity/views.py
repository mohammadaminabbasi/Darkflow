from df.DFResponse import DFResponse
from songsapi.models import *


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
