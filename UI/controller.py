import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        allGenres = self._model._genres
        for g in allGenres:
            self._view._ddGenre.options.append(ft.dropdown.Option(g))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        genre = self._view._ddGenre.value
        if genre is None:
            self._view.create_alert("Seleziona un genere")
            return
        self._model.buildGraph(genre)
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene {nNodes} nodi e {nEdges} archi"))
        bestTrack, max_degree = self._model.getMaxDegree()
        if bestTrack is None:
            self._view.txt_result.controls.append(ft.Text("Non esiste brano di grado massimo nel grafo"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(ft.Text(f"Il brano di grado massimo è {bestTrack} con grado {max_degree}"))
        self._view.update_page()

    def handleCammino(self,e):
        pass