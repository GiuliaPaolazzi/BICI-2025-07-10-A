import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._prodotti= []
        self._idMapProd={}
        self._bestPath= []
        self._bestScore =0

    def getBestPath(self, start, end, lun):
        #pulizia
        self._bestPath = []
        self._bestScore = 0
        #inizio
        parziale =[start]
        self._ricorsione(parziale, lun, end)
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, lun, end):
        # 1 verifico se parziale è solu valida e in caso la salvo
        if len(parziale) == lun:  # potenzialmente soluzione
            #verifico migliore
            if parziale[-1] == end and self._getScore(parziale) > self._bestScore:
                self._bestPath = copy.deepcopy(parziale)
                self._bestScore = self._getScore(parziale)
            return
        for n in self._grafo.successors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, lun, end)
                parziale.pop()

    def _getScore(self, parziale):
        score =0
        for i in range(0, len(parziale)-1):
            score += self._grafo[parziale[i]][parziale[i+1]]['weight']
        return score



    def getAllNodes(self):
        return self._grafo.nodes
    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        categories = DAO.getAllCategories()
        return categories
    def getProdottiDaCategoria(self, categoria):
        self._prodotti = DAO.getAllProductsConCategoria(categoria)
        for p in self._prodotti:
            self._idMapProd[p.product_id] = p
        return self._prodotti

    def buildGraph(self, categoria, data1, data2):
        self._grafo.clear()
        nodi= self.getProdottiDaCategoria(categoria)
        self._grafo.add_nodes_from(nodi)
        allEdges= DAO.getAllEdges(categoria, data1, data2, self._idMapProd)
        for e in allEdges:
            self._grafo.add_edge(e.p1, e.p2, weight=e.peso)



    def getNumNodi(self):
        return len(self._grafo.nodes)
    def getNumEdges(self):
        return len(self._grafo.edges)
    def getNodiPiuVenduti(self):
        listaNodiPesata = []
        for n in self._grafo.nodes:
            score = 0
            for e in self._grafo.out_edges(n, data=True):
                score += e[2]['weight']
            for e in self._grafo.in_edges(n, data=True):
                score -= e[2]['weight']
            listaNodiPesata.append((n, score))
        listaNodiPesata.sort(key=lambda x: x[1], reverse=True)
        return listaNodiPesata[0:5]



