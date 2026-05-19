import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._listGenre = None
        self.loadGenre()
        self._graph = nx.DiGraph()
        self._nodes = None
        self._edges = None
        self._idMapArt = {}

    def buildGraph(self, genre):
        self._graph.clear()
        self._nodes = DAO.getAllArtists()
        self.fillIdMap()
        self._graph.add_nodes_from(self._nodes)
        self._edges = DAO.getEdges(genre)
        for e in self._edges:
            a1 = self._idMapArt[e['idA']]
            a2 = self._idMapArt[e['idB']]
            peso =

    def fillIdMap(self):
        for n in self._nodes:
            self._idMapArt[n.ArtistId] = n
    def loadGenre(self):
        self._listGenre = DAO.getAllGenre()


    @property
    def listGenre(self):
        return self._listGenre