import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDStores(self):
        try:
            store = self._model.getAllStores()
            for y in store:
                self._view._ddStore.options.append(ft.dropdown.Option(y.store_name))
                # key=actor.id,
                #  text=actor.name))
           # self._view.update_page()

        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore nel recupero dello STORE: {ex}", color="red"))
            self._view.update_page()



    def handleCreaGrafo(self, e):
        store = self._view._ddStore.value

        if not store:
            self._view.create_alert("Selezionare lo STORE prima di creare il grafo.", color="red")
            return

        k = self._view._txtIntK.value
        # qui dovremmo fare i solti controlli sulla validità
        try:
            kInt = int(k)
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore ! devi inserire un intero per procedere: {ex}", color="red")
            )
            self._view.update_page()
            return

        if kInt <= 0:
            self._view.create_alert(
                "N deve essere un intero positivo.", color="red")
            return

        try:
            self._model.creaGrafo(store, kInt)
            n_nodes = self._model.get_num_nodes()
            n_edges = self._model.get_num_edges()
            # Stampa immediata numero di vertici e archi (Punto 1.c)
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(f"Grafo creato con successo!\nNumero vertici: {n_nodes}\nNumero archi: {n_edges}",
                        color="green"))
            # RIEMPIO IL DROPDOWN DEI nodi DEL GRAFO
            self.fillDDNodes()

        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore durante la creazione del grafo: {ex}", color="red"))
            # return
        self._view._txt_result.controls.clear()
        return

        # C) 3 ARCHI CON PESO MAGGIORE
        top5 = self._model.getTop5Archi()
        # self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f" 3 Archi di peso maggiore ", color="green"))

        # self._view._txt_result.controls.append(ft.Text(f"{arco[0]}-->{arco[1]} (peso: {arco[2]["weight"]})"))
        for i, arco in enumerate(top5, start=1):
            a1, a2, dati = arco
            self._view._txt_result.controls.append(ft.Text(
                f"{i})  Arco: {a1.order_id}   --> {a2.order_id}   )"
                f" - peso: {dati['weight']}")
            )
        self._view.update_page()

    def handleCerca(self, e):
        self._view._txt_result.controls.clear()
        # 1. Verifica che il grafo sia stato creato
        n_nodes, _ = self._model.getGraphDetails()
        if n_nodes == 0:
            self._view._txt_result.controls.append(
                ft.Text("Prima di cercare il percorso, devi creare il grafo!", color="red"))
            self._view.update_page()
            return

        # 2. Verifica selezione del nodo
        order_id_val = self._view._ddNode.value
        if not order_id_val:
            self._view._txt_result.controls.append(
                ft.Text("Selezionare un ordine/nodo di partenza dal menù a tendina.", color="red")
            )
            self._view.update_page()
            return

        # 3. Cerco il cammino più lungo
        source_node = self._model.getNodo(order_id_val)
        percorso = self._model.getPercorsoMassimo(source_node)

        # 4. Visualizzo il risultato
        self._view._txt_result.controls.append( ft.Text("Cammino più lungo:", weight="bold") )

        for ordine in percorso:
            self._view._txt_result.controls.append(
                ft.Text(f"Ordine {ordine.order_id} - Data: {ordine.order_date}") )

        self._view._txt_result.controls.append( ft.Text(f"Lunghezza del cammino: {len(percorso) - 1} archi") )
        self._view.update_page()

    def handleRicorsione(self, e):
        self._view._txt_result.controls.clear()

        if self._model.get_num_nodes() == 0 or self._model.get_num_edges() is None:
            self._view.create_alert("Creare prima il grafo!", color="red")
            return

        # Verifico che sia stato selezionato un nodo
        order_id_val = self._view._ddNode.value

        if not order_id_val:
            self._view._txt_result.controls.append(
                ft.Text("Selezionare un ordine di partenza.", color="red") )
            self._view.update_page()
            return

        # Recupero l'oggetto Order dal suo ID
        source_node = self._model.getNodo(order_id_val)

        # Calcolo il percorso di peso massimo
        percorso = self._model.getPercorsoPesoMassimo(source_node)

        # Visualizzo il risultato
        self._view._txt_result.controls.append(
            ft.Text("Percorso di peso massimo:", weight="bold", color="orange")
        )

        for i in range(len(percorso)):
            self._view._txt_result.controls.append(
                ft.Text( f"Ordine {percorso[i].order_id} - " f"Data: {percorso[i].order_date}" ) )

            if i < len(percorso) - 1:
                vicino = percorso[i + 1]
                peso_arco = self._model._grafo[percorso[i]][vicino]["weight"]

                self._view._txt_result.controls.append(
                    ft.Text(f"    ↓ peso: {peso_arco}")
                )
        peso = self._model.pesoMigliore
        self._view._txt_result.controls.append(
            ft.Text(f"Peso totale: {peso}", weight="bold", color="orange" ))

        self._view.update_page()

    def fillDDNodes(self):
        try:
            nodi = self._model.getAllNodes()
            self._view._ddNode.options.clear()

            for nodo in nodi:
                self._view._ddNode.options.append(
                    ft.dropdown.Option(
                        key=str(nodo.order_id),
                        text=str(nodo.order_id) )  )

            self._view._ddNode.value = None
            self._view._ddNode.disabled = False
            self._view.update_page()

        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore nel recupero dei nodi: {ex}", color="red")
            )
            self._view.update_page()