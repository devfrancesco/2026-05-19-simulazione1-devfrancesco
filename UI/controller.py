import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        genreList = self._model._listGenre
        for g in genreList:
            self._view._ddGenre.options.append(ft.dropdown.Option(g))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        genre = self._view._ddGenre.value
        if genre is None:
            self._view.create_alert("Seleziona un genere!")
            return
        self._model.buildGraph(genre)
        n_nodi, n_archi, best, inf, top5 = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n_nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {n_archi}"))
        self._view.txt_result.controls.append(ft.Text(f"Artista più influente: {best}, influenza: {inf}"))
        self._view.txt_result.controls.append(ft.Text(f"Top 5 archi:"))
        for u,v,w in top5:
            self._view.txt_result.controls.append(ft.Text(f"{u.Name} -> {v.Name} : {w}"))
        self._view.update_page()

    def handleCammino(self,e):
        pass

    # def fillDDArtist(self):
    #     genre = self._view._ddGenre.value
    #     if genre is None:
    #         self._view.create_alert("Attenzione! Seleziona un genere")
    #         self._view.update_page()
    #         return
    #     artistsList = self._model._listArtist