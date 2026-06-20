import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDCountry(self):
        countryList = self._model._listCountries
        for c in countryList:
            self._view._ddCountry.options.append(ft.dropdown.Option(c))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        country = self._view._ddCountry.value
        if country is None:
            self._view.create_alert("Seleziona una nazione!")
            self._view.update_page()
            return
        self._model.buildGraph(country)
        n_nodi, n_archi = self._model.getGraphDetails()
        bestEmp, archi_usc = self._model.getTopEmployee()
        minori3 = self._model.getSortedEdges()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n_nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {n_archi}"))
        self._view.txt_result.controls.append(ft.Text(f"Dipendente con più archi uscenti: {bestEmp} con {archi_usc} archi uscenti."))
        self._view.txt_result.controls.append(ft.Text("I 3 archi con peso minore:"))
        for a in minori3:
            self._view.txt_result.controls.append(ft.Text(f"{a[0]} -> {a[1]} : {a[2]['weight']:.2f}"))
        self.fillDDEmployee()
        self._view.update_page()

    def handleCammino(self,e):
        self._view.txt_result.controls.clear()
        employee = self._view._ddEmployee.value
        if employee is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona un dipendente."))
            self._view.update_page()
            return
        empId = int(employee)
        listOptEmp, maxClienti = self._model.getBestPath(empId)
        if len(listOptEmp) <= 1:
            self._view.txt_result.controls.append(
                ft.Text("Impossibile trovare un cammino oltre il dipendente di partenza."))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(ft.Text(f"Cammino ottimo trovato! Numero clienti totali: {maxClienti}"))
        for e in listOptEmp:
            self._view.txt_result.controls.append(ft.Text(e))
        self._view.update_page()

    def fillDDEmployee(self):
        self._view._ddEmployee.options.clear()
        for em in self._model._employees:
            self._view._ddEmployee.options.append(ft.dropdown.Option(key=em.EmployeeId, text=em))
        self._view.update_page()