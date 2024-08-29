import flet as ft
from Funcoes import Verificar_Diretorio

def main(page: ft.page):
    page.title = "Automação"
    page.window.width = 605
    page.window.height = 580
    page.window.center()
    page.window.to_front()
    page.window.resizable = False
    page.window.maximizable = False
    page.bgcolor = ft.colors.WHITE
    page.update()

    def btn_clicked(e):
        
        if txt1.value == '':
            txt1.error_text = "Campo Obrigatório"
            page.window.height = 605
        elif txt1.value.isnumeric() == False:
            txt1.error_text = "Digite Somente números"
            page.window.height = 605
        elif len(txt1.value) != 5:
            txt1.error_text = "O Código deve ter 5 digitos"
            page.window.height = 605
        else:
            page.window.height = 580
            txt1.error_text = None

        if txt2.value == '':
            txt2.error_text = "Campo Obrigatório"
            page.window.height = 605
        elif txt2.value.isnumeric() == False:
            txt2.error_text = "Digite Somente números"
            page.window.height = 605
        elif len(txt2.value) != 5:
            txt2.error_text = "O Código deve ter 5 digitos"
            page.window.height = 605
        else:
            page.window.height = 580
            txt2.error_text = None
        
        page.update()

        if ((txt1.value != '' and txt1.value.isnumeric() == True and len(txt1.value) == 5) and 
              (txt2.value != '' and txt2.value.isnumeric() == True and len(txt2.value) == 5)):
            
            btn1.tooltip = "Programa em Execução"
            btn1.disabled = True
            txt1.disabled = True
            txt2.disabled = True

            page.update()
            
            Verificar_Diretorio(int(txt1.value), int(txt2.value), txt3, txt1, txt2)      
        
    txt1 = ft.TextField(label="Último Código Fornecedor", width=240)
    txt2 = ft.TextField(label="Último Código Cliente", width=240)
    txt3 = ft.TextField(label="Output", width=500, read_only=True, bgcolor=ft.colors.GREY_300, multiline=True, min_lines=12, max_lines=12)

    btn1 = ft.ElevatedButton(
        text="Iniciar",
        width=500,
        height=50,
        bgcolor=ft.colors.GREEN_500,
        color=ft.colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5)
        ),
        on_click=btn_clicked
    )

    linha = ft.Row(controls=[txt1, txt2], spacing=20, alignment=ft.MainAxisAlignment.CENTER)

    container = ft.Container(
        content=ft.Column(
            controls=[
                linha,
                btn1,
                txt3                                                                   
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
