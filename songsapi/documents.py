from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from songsapi.models import *


@registry.register_document
class DFSongDocument(Document):
    class Index:
        name = 'dfsong'

    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }

    class Django:
        model = DFSong
        fields = [
            'id',
            'title',
            'artist',
            'songUrl',
            'imageUrl',
            'lyric',
            'likes',
            'genre',
        ]


@registry.register_document
class CommentDocument(Document):
    class Index:
        name = 'comment'

    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }

    class Django:
        model = Comment
        fields = [
            'id',
            'song_id',
            'user_id',
            'Comment',
        ]


@registry.register_document
class UserListenSongDocument(Document):
    class Index:
        name = 'user_listen_song'

    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }

    class Django:
        model = UserListenSong
        fields = [
            'song_id',
            'user_id'
        ]