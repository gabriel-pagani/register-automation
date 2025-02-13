import flet as ft
import pyodbc
from pyodbc import connect
from Funcoes import Verificar_Diretorio
from threading import Thread

running = True  # Variável global de controle
verificacao_thread = None  # Variável para controlar a thread


def main(page: ft.Page):
    page.title = "Automação"
    page.window.width = 605
    page.window.height = 600
    page.window.center()
    page.window.to_front()
    page.window.resizable = False
    page.window.maximizable = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    page.window.icon = r'C:\Users\gabriel.souza\AUTOMACAO\Imagens\logoRM.ico'
    page.update()

    global running, verificacao_thread

    def Search(e):
        conn_str = (
            "DRIVER={driverservidor};"
            "SERVER=ipservidor;"
            "DATABASE=basededados;"
            "UID=usuario;"
            "PWD=senha;"
        )
        query = """
        DECLARE @Codcoligada INT = 5;
        SELECT
        (SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'F%' and CODCOLIGADA = @Codcoligada ORDER BY DATACRIACAO DESC, CODCFO DESC) AS COD_FOR,
        (SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'C%' and CODCOLIGADA = @Codcoligada ORDER BY DATACRIACAO DESC, CODCFO DESC) AS COD_CLI;
        """
        try:
            with connect(conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                row = cursor.fetchone()
                txt1.value = row.COD_FOR
                txt2.value = row.COD_CLI
                page.update()
        except pyodbc.Error as e:
            txt3.value += f"Erro ao conectar ao banco de dados: {e}\n"
            txt3.update()

    def Start(e):

        global running, verificacao_thread
        running = True

        if (txt1.value != '' and txt2.value != ''):
            page.window.height = 600

            txt1.tooltip = "Programa em Execução"
            txt2.tooltip = "Programa em Execução"

            btn1.bgcolor = ft.Colors.GREY_300
            btn1.disabled = True
            btn1.tooltip = "Programa em Execução"

            btn2.bgcolor = ft.Colors.BLUE_900
            btn2.disabled = False

            swt.active_track_color = ft.Colors.GREY_300
            swt.disabled = True
            swt.tooltip = 'Programa em Execução'
            page.update()

            # Remove as letras do value do txt1 e txt2, deixando apenas os números
            codfor = txt1.value[1:]
            codcli = txt2.value[1:]

            # Cria uma nova thread para executar a função
            verificacao_thread = Thread(target=Verificar_Diretorio, args=(
                int(codfor), int(codcli), txt3, txt1, txt2, swt.value, lambda: running))
            verificacao_thread.start()

    def Restart(e):
        global running, verificacao_thread
        running = False

        swt.disabled = False
        swt.active_track_color = ft.Colors.GREEN
        swt.tooltip = 'Habilita/Desabilita o Salvamento Automático'

        txt1.value = ""
        txt2.value = ""
        txt3.value = ""

        btn1.bgcolor = ft.Colors.BLUE_900
        btn1.disabled = False
        btn1.tooltip = 'Inicia o Programa'

        btn2.bgcolor = ft.Colors.GREY_300
        btn2.disabled = True

        page.window.height = 600
        page.update()

        # Espera a thread finalizar (se houver uma em execução)
        if verificacao_thread is not None:
            verificacao_thread.join()

    txt1 = ft.TextField(label="Código Fornecedor",
                        width=205, bgcolor=ft.Colors.GREY_200, read_only=True)
    txt2 = ft.TextField(label="Código Cliente",
                        width=205, bgcolor=ft.Colors.GREY_200, read_only=True)
    txt3 = ft.TextField(label="Output", width=500,
                        read_only=True, bgcolor=ft.Colors.GREY_200, multiline=True, max_lines=10, min_lines=10)

    btn1 = ft.ElevatedButton(tooltip='Inicia o Programar', text="Iniciar", width=430, height=50, bgcolor=ft.Colors.BLUE_900,
                             color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=Start)
    btn2 = ft.ElevatedButton(tooltip='Reinicia o Programar', text="Reiniciar", width=500, height=50, bgcolor=ft.Colors.GREY_300,
                             color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=Restart, disabled=True)

    iconbtn1 = ft.IconButton(icon=ft.Icons.SEARCH, height=50, width=50, icon_size=30, on_click=Search,
                             tooltip='Busca os Códigos no Banco de Dados',)

    swt = ft.Switch(value=True, tooltip='Habilita/Desabilita o Salvamento Automático',
                    active_track_color=ft.Colors.GREEN)

    linha = ft.Row(controls=[txt1, iconbtn1, txt2], spacing=20,
                   alignment=ft.MainAxisAlignment.CENTER)
    linha2 = ft.Row(controls=[btn1, swt], spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER)

    container = ft.Container(
        content=ft.Column(
            controls=[
                linha,
                linha2,
                txt3,
                btn2,
            ],
            width=500,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        expand=True,
        width=600,
        alignment=ft.alignment.center
    )

    page.add(container)


ft.app(target=main, assets_dir="assets")
