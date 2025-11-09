import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMapO = {}

    def  getAllStores(self):
        return DAO.getAllStores()

    def creaGrafo(self, store_name, K):
        self._grafo.clear()
        self._idMapO.clear()

        ordini = DAO.getAllNodes(store_name)
        for a in ordini:
            self._idMapO[a. order_id] = a
            self._grafo.add_node(a)
            # aggiungo i nodi
        print("2 - Nodi aggiunti")

        # 3. Calcolo il numero di oggetti di ogni ordine
        numOggetti = {}

        for o in ordini:
            numOggetti[o.order_id] = DAO.getNumeroOggetti(o.order_id)

            # 4. Confronto tutte le coppie di ordini
        for i in range(len(ordini)):
            o1 = ordini[i]
            for j in range(i + 1, len(ordini)):
                o2 = ordini[j]

                # 5. Calcolo la distanza temporale
                giorni = abs((o2.order_date - o1.order_date).days)

                # 6. Verifico il vincolo temporale
                if giorni <= K and giorni > 0:

                    # 7. Calcolo il peso dell'arco
                    peso = (numOggetti[o1.order_id] +numOggetti[o2.order_id] ) / giorni

                    # 8. Aggiungo l'arco nella direzione corretta
                    if o1.order_date < o2.order_date:
                        self._grafo.add_edge(o1, o2, weight=peso)
                    else:
                        self._grafo.add_edge(o2, o1, weight=peso)

        print("Archi aggiunti:", self._grafo.number_of_edges())

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_num_nodes(self) -> int:
        return self._grafo.number_of_nodes()

    def get_num_edges(self) -> int:
        return self._grafo.number_of_edges()

    def getAllNodes(self):
        return list(self._grafo.nodes)

    def getTop5Archi(self):
        # return sorted(self._grafo.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:10]
        archi = self._grafo.edges(data=True)
        return sorted(
            archi,
            key=lambda x: x[2]["weight"],
            reverse=True
        )[:5]

    def getNodo(self, order_id):
        return self._idMapO[int(order_id)]

    def getPercorsoMassimo(self, source_node): #dfs -- TROVA CAMMINO MAX NELL'ALBEROO, non per forza nel grafo
        # 1. Costruisce l'albero di visita DFS a partire dal nodo sorgente
        tree = nx.dfs_tree(self._grafo, source=source_node)

        # Se il nodo non ha archi uscenti, l'albero contiene solo se stesso
        if len(tree.nodes) <= 1:
            return []

        # 2. Trova le foglie dell'albero (nodi con grado uscente pari a 0)
        foglie = [nodo for nodo in tree.nodes if tree.out_degree(nodo) == 0 and nodo != source_node]

        # 3. Trova il cammino più lungo tra la sorgente e tutte le foglie
        cammino_massimo = []
        for foglia in foglie:
            # In un albero orientato esiste esattamente UN solo percorso tra radice e foglia
            path = nx.shortest_path(tree, source=source_node, target=foglia)
            if len(path) > len(cammino_massimo):
                cammino_massimo = path

        return cammino_massimo

    def getPercorsoMassimoV2(self, order_id):
        # Recupero il nodo di partenza
        nodo = self._idMapO[int(order_id)]
        percorsoMigliore = []

        def DFS(nodo, percorso):
            nonlocal percorsoMigliore

            # Aggiungo il nodo al percorso corrente
            percorso.append(nodo)

            # Se il percorso è il più lungo trovato, lo salvo
            if len(percorso) > len(percorsoMigliore):
                percorsoMigliore = percorso.copy()

            # Esploro i nodi raggiungibili
            for vicino in self._grafo.successors(nodo):
                if vicino not in percorso:
                    DFS(vicino, percorso)

            # Torno indietro per provare un altro percorso
            percorso.pop()

        DFS(nodo, [])

        return percorsoMigliore

    def getPercorsoPesoMassimo(self, source_node):
        self.camminoMigliore = [source_node]
        self.pesoMigliore = 0

        self._ricorsione(source_node, [source_node], float("inf"), 0)

        return self.camminoMigliore

    def _ricorsione(self, nodo, cammino, pesoPrecedente, pesoTotale):

        if pesoTotale > self.pesoMigliore:
            self.pesoMigliore = pesoTotale
            self.camminoMigliore = cammino.copy()

        for vicino in self._grafo.successors(nodo):
            peso = self._grafo[nodo][vicino]["weight"]

            if vicino not in cammino and peso < pesoPrecedente:
                cammino.append(vicino)

                self._ricorsione(
                    vicino,
                    cammino,
                    peso,
                    pesoTotale + peso
                )

                cammino.pop()

