import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._genres = DAO.getAllGenre()
        self._graph = nx.Graph()
        self._tracks = []
        self._idMapT = {}

    def buildGraph(self, genre):
        self._graph.clear()
        self._idMapT = {}
        self._tracks = DAO.getAllTracks(genre)
        self._graph.add_nodes_from(self._tracks)
        for track in self._tracks:
            self._idMapT[track.TrackId] = track
        allEdges = DAO.getAllEdges(genre, self._idMapT)
        for e in allEdges:
            self._graph.add_edge(e.t1, e.t2, weight=e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getMaxDegree(self):
        if len(self._graph.nodes) == 0:
            return None, 0
        best_track = max(self._graph.nodes, key=self._graph.degree)
        max_degree = self._graph.degree(best_track)
        return best_track, max_degree
