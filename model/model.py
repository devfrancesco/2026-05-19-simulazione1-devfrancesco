import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._listCountries = DAO.getAllCountry()
        self._employees = []
        self._idMapEmp = {}
        self._clientiMappa = {}
        self._optPath = []
        self._maxClienti = -1

    def getBestPath(self, dipendente_iniziale):
        self._optPath = []
        self._maxClienti = -1
        dipendenteP = self._idMapEmp[dipendente_iniziale] #lo possiamo fare perchè abbiamo salvato il dipendente come id
        parziale = [dipendenteP]
        self._ricorsione(parziale, 0.0) #0.0 è il costo
        return self._optPath, self._maxClienti

    def _ricorsione(self, parziale, costo_attuale):
        if costo_attuale > 50.0:
            return
        clienti_potenziali = self._calcolo_clienti_cammino(parziale)
        if clienti_potenziali > self._maxClienti:
            self._optPath = copy.deepcopy(parziale)
            self._maxClienti = clienti_potenziali
        nodo_corrente = parziale[-1]
        for vicino in self._graph.neighbors(nodo_corrente):
            if vicino not in parziale:
                peso_arco = self._graph[nodo_corrente][vicino]['weight']
                parziale.append(vicino)
                self._ricorsione(parziale, costo_attuale + peso_arco)
                parziale.pop()

    def _calcolo_clienti_cammino(self, cammino):
        somma_clienti = 0
        for emp in cammino:
            num_clienti = self._clientiMappa.get(emp.EmployeeId, 0)
            somma_clienti += num_clienti
        return somma_clienti


    def buildGraph(self, country):
        self._graph.clear()
        self._idMapEmp.clear()
        self._employees = DAO.getAllEmployee(country)
        self._clientiMappa = DAO.getClientiPerDipendente(country)
        for e in self._employees:
            self._idMapEmp[e.EmployeeId] = e
            self._graph.add_node(e)
        allEdges = DAO.getllArchi(country, self._idMapEmp)
        for e in allEdges:
            self._graph.add_edge(e.e1, e.e2, weight= e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getTopEmployee(self):
        if self._graph.nodes == 0:
            return None, 0
        bestEmp = None
        max_out = -1
        for emp in self._graph.nodes:
            archi_uscenti = self._graph.out_degree(emp)
            if archi_uscenti > max_out:
                max_out = archi_uscenti
                bestEmp = emp
        return bestEmp, max_out

    def getSortedEdges(self):
        archi = list(self._graph.edges(data=True))
        archi.sort(key=lambda x: x[2]['weight'])
        return archi[:3] # i primi 3


