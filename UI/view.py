import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Simulazione d'Esame - Gestione Store Commerciale"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("TdP - Analisi Relazioni Commerciali", color="blue", size=24)
        self._page.controls.append(self._title)

        # Riga 1: Selezione Nazione e Creazione Grafo
        self._ddCountry = ft.Dropdown(label="Nazione", width=250)
        self._controller.fillDDCountry()  # Popola le nazioni dei clienti
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo",
                                               on_click=self._controller.handleCreaGrafo, width=250)

        row1 = ft.Row([self._ddCountry, self._btnCreaGrafo],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # Riga 2: Selezione Dipendente e Ricerca Cammino
        self._ddEmployee = ft.Dropdown(label="Dipendente", width=250)
        self._btnTrovaCammino = ft.ElevatedButton(text="Trova Cammino",
                                                  on_click=self._controller.handleCammino, width=250)

        row2 = ft.Row([self._ddEmployee, self._btnTrovaCammino],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()