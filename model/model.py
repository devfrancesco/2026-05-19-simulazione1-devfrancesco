import copy
import heapq

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapArt = {}
        self._listGenre = DAO.getAllGenre()
        self._artists = []
        self._optPath = []

    def getMaxPath(self, artista_partenza):
        self._optPath = []
        parziale = [artista_partenza]
        self._ricorsione(parziale, peso_prec = -1) #nessun arco può avere peso megativo
        return self._optPath

    def _ricorsione(self, parziale, peso_prec):
        if len(parziale) > len(self._optPath):
            self._optPath = copy.deepcopy(parziale)
        nodo_corrente = parziale[-1]
        for vicino in self._graph.neighbors(nodo_corrente): #solo archi uscenti
            dati_arco = self._graph.get_edge_data(nodo_corrente, vicino)
            peso_arco_corrente = dati_arco['weight'] #peso
            if peso_arco_corrente > peso_prec:
                if vicino not in parziale:
                    parziale.append(vicino)
                    self._ricorsione(parziale, peso_arco_corrente)
                    parziale.pop()

        # predecessore = self._graph.predecessors(nodo_corrente)
        # self._graph.get_edge_data(predecessore, nodo_corrente)


    def buildGraph(self, genre):
        self._graph.clear()
        self._idMapArt.clear()
        self._artists = DAO.getArtistsPopolarita(genre)
        for a in self._artists:
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

    def getTop(self):
        if self._graph.nodes == 0:
            return None, 0, []
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
        top5 = sorted(self._graph.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)[:5]
        return bestArtist, bestInfluenza, top5

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllArtists(self):
        return self._artists

