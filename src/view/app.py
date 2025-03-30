import flet as ft


class App:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.setup_page()
        self.show_interface()

    def setup_page(self) -> None:
        self.page.title = 'Automação'
        self.page.window.width = 600
        self.page.window.height = 250
        self.page.window.center()
        self.page.window.to_front()
        self.page.window.resizable = False
        self.page.window.maximizable = False
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = ft.Colors.WHITE
        self.page.update()

    def show_interface(self) -> None:

        # Components
        client_code = ft.TextField(
            label="Código Fornecedor",
            width=205,
            read_only=True,
        )
        supplier_code = ft.TextField(
            label="Código Cliente",
            width=205,
            read_only=True,
        )
        start_button = ft.ElevatedButton(
            text="Iniciar",
            width=430,
            height=50,
            bgcolor=ft.Colors.BLUE_900,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5)
            ),
        )
        restart_button = ft.ElevatedButton(
            text="Reiniciar",
            width=210,
            height=50,
            bgcolor=ft.Colors.GREY_300,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5)
            ),
            disabled=True,
        )
        search_button = ft.IconButton(
            icon=ft.Icons.SEARCH,
            height=50,
            width=50,
            icon_size=30,
            tooltip='Busca os Códigos no Banco de Dados',
        )
        switch = ft.Switch(
            value=True,
            tooltip='Habilita/Desabilita o Salvamento Automático',
            active_track_color=ft.Colors.GREEN,
        )

        # Layout
        text_row = ft.Row(
            controls=[
                supplier_code,
                search_button,
                client_code,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        button_row = ft.Row(
            controls=[
                start_button,
                switch,
                # restart_button,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        container = ft.Container(
            content=ft.Column(
                controls=[
                    text_row,
                    button_row,
                ],
                width=500,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            width=600,
            alignment=ft.alignment.center,
        )

        self.page.add(container)
