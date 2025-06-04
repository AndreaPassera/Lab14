import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillddStore(self):
        for s in self._model.getStore():
             self._view._ddStore.options.append(ft.dropdown.Option(s["store_id"]))
        self._view.update_page()
    def handleCreaGrafo(self, e):
        store=self._view._ddStore.value
        if store is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Attenzione, selezionare un valore"))
            self._view.update_page()
            return

        lun=self._view._txtIntK.value
        if lun =="":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Attenzione, inserire un valore"))
            self._view.update_page()
            return

        try:
            intLun= int(lun)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Attenzione, inserire un numero intero"))
            self._view.update_page()
            return

        self._model.buildGraph(int(store),intLun)
        self._view._ddNode.options.clear()
        for n in self._model.grafo.nodes():
            self._view._ddNode.options.append(ft.dropdown.Option(n.order_id))
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        n,a=self._model.getGraphDetails()
        self._view._txt_result.controls.append(ft.Text(f"Numero nodi: {n}, Numero archi: {a}"))
        self._view.update_page()



    def handleCerca(self, e):
        source=self._view._ddNode.value
        if source is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Attenzione, selezionare un valore"))
            self._view.update_page()
            return

        cammino=self._model.getCamminoMax(int(source))
        self._view._txt_result.controls.append(ft.Text(f"Cammino a partire da {source}"))
        for n in cammino:
            self._view._txt_result.controls.append(ft.Text(n.order_id))
        self._view.update_page()

    def handleRicorsione(self, e):
        pass
