import flet as ft
from Funcoes import Verificar_Diretorio
from threading import Thread

running = True  # Variável global de controle
verificacao_thread = None  # Variável para controlar a thread


def main(page: ft.Page):
    page.title = "Automação"
    page.window.width = 605
    page.window.height = 390
    page.window.center()
    page.window.to_front()
    page.window.resizable = False
    page.window.maximizable = False
    page.bgcolor = ft.Colors.WHITE
    page.update()

    global running, verificacao_thread

    def btn_clicked(e):

        global running, verificacao_thread
        running = True

        if txt1.value == '':
            txt1.error_text = "Campo Obrigatório"
            page.window.height = 415
        elif txt1.value.isnumeric() == False:
            txt1.error_text = "Digite Somente números"
            page.window.height = 415
        elif len(txt1.value) > 5:
            txt1.error_text = "O Código deve ter até 5 digitos"
            page.window.height = 415
        else:
            txt1.error_text = None

        if txt2.value == '':
            txt2.error_text = "Campo Obrigatório"
            page.window.height = 415
        elif txt2.value.isnumeric() == False:
            txt2.error_text = "Digite Somente números"
            page.window.height = 415
        elif len(txt2.value) > 5:
            txt2.error_text = "O Código deve ter até 5 digitos"
            page.window.height = 415
        else:
            txt2.error_text = None

        page.update()

        if ((txt1.value != '' and txt1.value.isnumeric() == True and len(txt1.value) <= 5) and
                (txt2.value != '' and txt2.value.isnumeric() == True and len(txt2.value) <= 5)):
            page.window.height = 390

            txt1.disabled = True
            txt1.tooltip = "Programa em Execução"

            txt2.disabled = True
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

            # Cria uma nova thread para executar a função
            verificacao_thread = Thread(target=Verificar_Diretorio, args=(
                int(txt1.value), int(txt2.value), txt3, txt1, txt2, swt.value, lambda: running))
            verificacao_thread.start()

    def Restart(e):
        global running, verificacao_thread
        running = False

        swt.disabled = False
        swt.value = True
        swt.active_track_color = ft.Colors.GREEN
        swt.tooltip = 'Habilita/Desabilita o Salvamento Automático'

        txt1.error_text = None
        txt1.tooltip = None
        txt1.disabled = False
        txt1.value = ''

        txt2.error_text = None
        txt2.tooltip = None
        txt2.disabled = False
        txt2.value = ''

        txt3.value = ' '

        btn1.bgcolor = ft.Colors.BLUE_900
        btn1.disabled = False
        btn1.tooltip = 'Inicia o Programa'

        btn2.bgcolor = ft.Colors.GREY_300
        btn2.disabled = True

        page.window.height = 390
        page.update()

        # Espera a thread finalizar (se houver uma em execução)
        if verificacao_thread is not None:
            verificacao_thread.join()

    txt1 = ft.TextField(label="Último Código Fornecedor", width=240)
    txt2 = ft.TextField(label="Último Código Cliente", width=240)
    txt3 = ft.TextField(value=" ", label="Output", width=500,
                        read_only=True, bgcolor=ft.Colors.GREY_200)

    btn1 = ft.ElevatedButton(tooltip='Inicia o Programar', text="Iniciar", width=435, height=50, bgcolor=ft.Colors.BLUE_900,
                             color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=btn_clicked)
    btn2 = ft.ElevatedButton(tooltip='Reinicia o Programar', text="Reiniciar", width=500, height=50, bgcolor=ft.Colors.GREY_300,
                             color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=Restart, disabled=True)

    swt = ft.Switch(value=True, tooltip='Habilita/Desabilita o Salvamento Automático',
                    active_track_color=ft.Colors.GREEN)

    linha = ft.Row(controls=[txt1, txt2], spacing=20,
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
