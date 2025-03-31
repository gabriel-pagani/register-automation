import flet as ft
from time import sleep
from src.utils.connection import server_request


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
        def search(e):
            response = server_request(
                query="""
                    SELECT
                        (SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'F%' and CODCOLIGADA = 5 ORDER BY DATACRIACAO DESC, CODCFO DESC) AS COD_FOR,
                        (SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'C%' and CODCOLIGADA = 5 ORDER BY DATACRIACAO DESC, CODCFO DESC) AS COD_CLI;
                """
            )
            supplier_code.value = response['data'][0]['COD_FOR']
            client_code.value = response['data'][0]['COD_CLI']
            self.page.update()

        def start(e):
            if (supplier_code.value != '' and client_code.value != ''):
                start_button.bgcolor = ft.Colors.GREY_300
                start_button.tooltip = 'Automação em Execução'
                start_button.disabled = True
                search_button.tooltip = 'Automação em Execução'
                search_button.disabled = True
                restart_button.bgcolor = ft.Colors.BLUE_900
                restart_button.disabled = False
                self.page.update()

                # Adicionar a automação aqui!

            else:
                supplier_code.error_text = "Campo em branco!"
                client_code.error_text = "Campo em branco!"
                self.page.update()
                sleep(2)
                supplier_code.error_text = None
                client_code.error_text = None
                self.page.update()

        def restart(e):
            supplier_code.value = ''
            client_code.value = ''
            start_button.bgcolor = ft.Colors.BLUE_900
            start_button.tooltip = ''
            start_button.disabled = False
            search_button.tooltip = ''
            search_button.disabled = False
            restart_button.bgcolor = ft.Colors.GREY_300
            restart_button.disabled = True
            self.page.update()

            # Adicionar a lógica para reiniciar aqui!

        # Components
        client_code = ft.TextField(
            label="Código Cliente",
            width=205,
        )
        supplier_code = ft.TextField(
            label="Código Fornecedor",
            width=205,
        )
        start_button = ft.ElevatedButton(
            text="Iniciar",
            width=240,
            height=50,
            bgcolor=ft.Colors.BLUE_900,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5)
            ),
            on_click=start
        )
        restart_button = ft.ElevatedButton(
            text="Reiniciar",
            width=240,
            height=50,
            bgcolor=ft.Colors.GREY_300,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5)
            ),
            disabled=True,
            on_click=restart
        )
        search_button = ft.IconButton(
            icon=ft.Icons.SEARCH,
            height=50,
            width=50,
            icon_size=30,
            tooltip='Busca os Códigos no Banco de Dados',
            on_click=search,
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
                # switch,
                restart_button,
            ],
            spacing=20,
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
