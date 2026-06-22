import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceCategoria = None
        self._choiceProdStart = None
        self._choiceProdEnd = None
        # punto 2
        self._lunghezzaPercorso = 0
        self._bestCammino = []
        self._bestScore = 0

    def _fillDDCategories(self):
        categorie = self._model.getCategories()
        for c in categorie:
            self._view._ddcategory.options.append(ft.dropdown.Option(data=c,
                                                                    key=c.category_name,
                                                                    on_click=self._choiceDDCategoria))
    def _choiceDDCategoria(self, e):
        self._choiceCategoria = e.control.data
        print(f"Hai selezionato la categoria {self._choiceCategoria}")
    #2
    def _fillDDProdotti(self):
        prodotti = self._model.getAllNodes()
        for p in prodotti:
            self._view._ddProdStart.options.append(ft.dropdown.Option(data=p,
                                                                    key=p.product_name,
                                                                    on_click=self._choiceDDProdottoStart))
            self._view._ddProdEnd.options.append(ft.dropdown.Option(data=p,
                                                                      key=p.product_name,
                                                                      on_click=self._choiceDDProdottoEnd))

    def _choiceDDProdottoEnd(self, e):
        self._choiceProdEnd = e.control.data
        print(f"Hai selezionato come ultimo prod: {self._choiceProdEnd}")
    def _choiceDDProdottoStart(self, e):
        self._choiceProdStart = e.control.data
        print(f"Hai selezionato come prod di partenza: {self._choiceProdStart}")

    def handleCreaGrafo(self, e):
        #def parametri che devo passare al model
        cat=self._choiceCategoria
        data1= self._view._dp1.value
        data2= self._view._dp2.value
        self._model.buildGraph(cat,data1,data2)
        nN= self._model.getNumNodi()
        nA= self._model.getNumEdges()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Tra le date {self._view._dp1.value.date()} e {self._view._dp2.value.date()} "
                                                      f"grafo creato con {nN} nodi e {nA} archi "))
        self._fillDDProdotti()
        self._view.update_page()

    def handleLunghezzaPercorso(self):
        lun= self._view._txtInLun.value
        if lun == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Attenzione, Inserire valore di lunghezza del percorso!", color="red"))
            self._view.update_page()
            return
        try:
            lunInt = int(lun)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore numerico intero per la lunghezza", color="red"))
            self._view.update_page()
            return
        # controllo che sia positivo
        if lunInt < 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore numerico intero positivo per la lunghezza", color="red"))
            self._view.update_page()
        self._lunghezzaPercorso = lunInt




    def handleBestProdotti(self, e):
        bestProdotti = self._model.getNodiPiuVenduti()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Di seguito i nodi più profittevoli:"))
        for b in bestProdotti:
            self._view.txt_result.controls.append(
                ft.Text(f"{b[0]} - score {b[1]}"))

        self._view.update_page()

    def handleCercaCammino(self, e):
        self.handleLunghezzaPercorso()
        lun = self._lunghezzaPercorso
        start = self._choiceProdStart
        end = self._choiceProdEnd
        path, score = self._model.getBestPath(start, end, lun)
        self._view.txt_result.controls.clear()
        if len(path) == 0:
            self._view.txt_result.controls.append(ft.Text(f"Non ho trovato nessun cammino"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(ft.Text(f"Ecco il cammino con score {score}:"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))
        self._view.update_page()



    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
