import heapq

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapArt = {}
        self._listGenre = DAO.getAllGenre()


    def buildGraph(self, genre):
        self._graph.clear()
        self._idMapArt.clear()
        artists = DAO.getArtistsPopolarita(genre)
        for a in artists:
            self._idMapArt[a.ArtistId] = a
            self._graph.add_node(a)
        pairs = DAO.getConnectedPairs(genre)
        for idA, idB in pairs:
            if idA not in self._idMapArt or idB not in self._idMapArt:
                continue
            a = self._idMapArt[idA]
            b = self._idMapArt[idB]
            peso = a.popolarita + b.popolarita
            if a.popolarita >= b.popolarita:
                self._graph.add_edge(a,b, weight=peso)
            if a.popolarita <= b.popolarita:
                self._graph.add_edge(b,a, weight=peso)

    def getGraphDetails(self):
        n_nodi = self._graph.number_of_nodes()
        n_archi = self._graph.number_of_edges()
        if n_nodi == 0:
            return 0, 0, None, 0, []
        bestArtist = None
        bestInfluenza = None
        for artist in self._graph.nodes():
            # peso_out = sum(d['weight'] for _,_, d in self._graph.out_edges(artist, data=True))
            peso_out = self._graph.out_degree(artist, weight='weight')
            peso_in = self._graph.in_degree(artist, weight='weight')
            influenza = peso_out - peso_in
            if bestInfluenza is None or influenza > bestInfluenza:
                bestInfluenza = influenza
                bestArtist = artist
        # TOP 5
        all_edges = [(u, v, d['weight']) for u, v, d in self._graph.edges(data=True)]
        top5 = sorted(all_edges, key=lambda x: x[2], reverse=True)[:5]
        return n_nodi, n_archi, bestArtist, bestInfluenza, top5
