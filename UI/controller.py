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
        n_nodi, n_archi = self._model.getGraphDetails()
        best, inf, top5 = self._model.getTop()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n_nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {n_archi}"))
        self._view.txt_result.controls.append(ft.Text(f"Artista più influente: {best}, influenza: {inf}"))
        self._view.txt_result.controls.append(ft.Text(f"Top 5 archi:"))
        for e in top5:
            self._view.txt_result.controls.append(ft.Text(f"{e[0]} -> {e[1]} : {e[2]['weight']}"))
        self.fillDDArtists()
        self._view.update_page()

    def handleCammino(self,e):
        actor = self._view._ddArtist.value
        if actor is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Seleziona un attore dal menu a tendina.", color="red"))
            self._view.update_page()
            return
        self._view.txt_result.controls.clear()
        actor_id = int(actor)
        listOptActor = self._model.getMaxPath(actor_id)
        for a in listOptActor:
            self._view.txt_result.controls.append(ft.Text(a))
        self._view.update_page()

    def fillDDArtists(self):
        self._view._ddArtist.options.clear()
        for a in self._model.getAllArtists():
            self._view._ddArtist.options.append(ft.dropdown.Option(key=a.ArtistId, text=a))
        self._view.update_page()