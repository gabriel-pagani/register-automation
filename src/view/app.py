import flet as ft
from src.utils.Funcoes import Verificar_Diretorio


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
        def start(e):
            start_button.bgcolor = ft.Colors.GREY_300
            start_button.tooltip = 'Automação em Execução'
            start_button.disabled = True
            restart_button.bgcolor = ft.Colors.BLUE_900
            restart_button.disabled = False
            self.page.update()

            Verificar_Diretorio()

        def restart(e):
            start_button.bgcolor = ft.Colors.BLUE_900
            start_button.tooltip = ''
            start_button.disabled = False
            restart_button.bgcolor = ft.Colors.GREY_300
            restart_button.disabled = True
            self.page.update()

            # Implementar a lógica para reiniciar a automação aqui

        # Components
        start_button = ft.ElevatedButton(
            text="Iniciar",
            width=500,
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
            width=500,
            height=50,
            bgcolor=ft.Colors.GREY_300,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5)
            ),
            disabled=True,
            on_click=restart
        )
        container = ft.Container(
            content=ft.Column(
                controls=[
                    start_button,
                    restart_button,
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
