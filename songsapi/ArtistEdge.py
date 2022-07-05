import random

from django.db.models import Q

from songsapi.models import ArtistEdge
from songsapi.static_database_utils import get_artist


class ArtistGraph:
    def __init__(self, graph: [ArtistEdge]):
        self.graph = graph

    def __str__(self):
        for edge in self.graph:
            print(edge)

    def recommend_similar_artists(self, artist_name):
        result = []
        for i in range(0, 10):
            edges_contain_artist = ArtistEdge.objects \
                .filter(Q(artist1=artist_name) | Q(artist2=artist_name)) \
                .order_by('-weight')

            edges_contain_artist = edges_contain_artist[0:len(edges_contain_artist) * 0.6]

            selected_artist = random.choices(edges_contain_artist,
                                             weights=[edge.weight for edge in edges_contain_artist],
                                             k=1)
            artist_name = selected_artist
            result.append(get_artist(selected_artist))

        print(list(set(result)))
