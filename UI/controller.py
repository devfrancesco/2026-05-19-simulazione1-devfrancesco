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
        pass

    def handleCreaGrafo(self,e):
        pass

    def handleCammino(self,e):
        pass

    # def fillDDArtist(self):
    #     genre = self._view._ddGenre.value
    #     if genre is None:
    #         self._view.create_alert("Attenzione! Seleziona un genere")
    #         self._view.update_page()
    #         return
    #     artistsList = self._model._listArtist