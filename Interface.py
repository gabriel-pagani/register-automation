import flet as ft
from Funcoes import Verificar_Diretorio

def main(page: ft.page):
    page.title = "Automação"
    page.window.width = 605
    page.window.height = 650
    page.window.center()
    page.window.to_front()
    page.window.resizable = False
    page.window.maximizable = False
    page.bgcolor = ft.colors.WHITE
    page.update()

    def btn_clicked(e):
        
        if txt1.value == '':
            txt1.error_text = "Campo Obrigatório"
            page.window.height = 675
        elif txt1.value.isnumeric() == False:
            txt1.error_text = "Digite Somente números"
            page.window.height = 675
        elif len(txt1.value) != 5:
            txt1.error_text = "O Código deve ter 5 digitos"
            page.window.height = 675
        else:
            txt1.error_text = None

        if txt2.value == '':
            txt2.error_text = "Campo Obrigatório"
            page.window.height = 675
        elif txt2.value.isnumeric() == False:
            txt2.error_text = "Digite Somente números"
            page.window.height = 675
        elif len(txt2.value) != 5:
            txt2.error_text = "O Código deve ter 5 digitos"
            page.window.height = 675
        else:           
            txt2.error_text = None
        
        page.update()

        if ((txt1.value != '' and txt1.value.isnumeric() == True and len(txt1.value) == 5) and 
              (txt2.value != '' and txt2.value.isnumeric() == True and len(txt2.value) == 5)):          
            page.window.height = 650 
            txt1.disabled = True
            txt2.disabled = True
            btn1.disabled = True
            swt.disabled = True
            btn2.disabled = False
            txt1.tooltip = "Programa em Execução"
            txt2.tooltip = "Programa em Execução"
            btn1.tooltip = "Programa em Execução"
            swt.tooltip = 'Programa em Execução'
            page.update()
            
            Verificar_Diretorio(int(txt1.value), int(txt2.value), txt3, txt1, txt2, swt.value)      
        
    def Close(e):
        page.window.close()

    txt1 = ft.TextField(label="Último Código Fornecedor", width=240)
    txt2 = ft.TextField(label="Último Código Cliente", width=240)
    txt3 = ft.TextField(value=" ", label="Output", width=500, read_only=True, bgcolor=ft.colors.GREY_200, multiline=True, min_lines=12, max_lines=12)

    btn1 = ft.ElevatedButton(tooltip='Inicia o Programar',text="Iniciar",width=435,height=50,bgcolor=ft.colors.BLUE_900,color=ft.colors.WHITE,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),on_click=btn_clicked)
    btn2 = ft.ElevatedButton(tooltip='Finaliza o Programar',text="Encerrar",width=500,height=50,bgcolor=ft.colors.BLUE_900,color=ft.colors.WHITE,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),on_click=Close, disabled=True)
    
    swt = ft.Switch(value=True, tooltip='Habilita/Desabilita o Salvamento Automático', active_track_color=ft.colors.BLUE_900)

    linha = ft.Row(controls=[txt1, txt2], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
    linha2 = ft.Row(controls=[btn1, swt], spacing=10, alignment=ft.MainAxisAlignment.CENTER)

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
