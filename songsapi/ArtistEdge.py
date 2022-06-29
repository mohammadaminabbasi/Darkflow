from songsapi.models import ArtistEdge


class Graph:
    def __init__(self, graph: [ArtistEdge]):
        self.graph = graph

    def __str__(self):
        for edge in self.graph:
            print(edge)

    def search_edge_in_graph(self, special_edge: ArtistEdge):
        for edge in self.graph:
            if edge.artist1 == special_edge.artist1 and edge.artist2 == special_edge.artist2:
                return edge
            if edge.artist1 == special_edge.artist2 and edge.artist2 == special_edge.artist1:
                return edge
        return None

    def add_edge(self, edge: ArtistEdge):
        searched_edge = self.search_edge_in_graph(edge)
        if searched_edge is None:
            self.graph.append(edge)
        else:
            self.remove_edge(edge)
            searched_edge.weight = searched_edge.weight + 1
            self.graph.append(searched_edge)

    def remove_edge(self, special_edge: ArtistEdge):
        remove_index = -1
        for i, edge in enumerate(self.graph):
            if edge.artist1 == special_edge.artist1 and edge.artist2 == special_edge.artist2:
                remove_index = i
            elif edge.artist1 == special_edge.artist2 and edge.artist2 == special_edge.artist1:
                remove_index = i

        if remove_index != -1:
            self.graph.pop(remove_index)
        return None
