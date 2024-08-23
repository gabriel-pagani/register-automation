import flet as ft

def main(page: ft.page):
    page.title = "Menu Principal"
    page.window.width = 500
    page.window.height = 500
    page.window.resizable = False
    page.window.maximizable = False
    page.bgcolor = ft.colors.WHITE
    page.update()
    
    def arquivo_selecionados_resultado(e: ft.FilePickerResultEvent):
        arquivos = e.files
        for arquivo in arquivos:
            print(arquivo.path)

    arquivos_selecionados_dialog = ft.FilePicker(on_result=arquivo_selecionados_resultado)

    page.overlay.append(arquivos_selecionados_dialog)

    container = ft.Container(
        content=ft.Column(
            controls=[
                ft.TextField(label="Último Código Forecedor", width=300),
                ft.TextField(label="Último Código Cliente", width=300),
                ft.ElevatedButton(text="Selecionar Arquivos", 
                    width=300,
                    height=50,
                    bgcolor=ft.colors.GREY_100, 
                    icon=ft.icons.UPLOAD_FILE, 
                    on_click=lambda _: arquivos_selecionados_dialog.pick_files(
                        allow_multiple=True, 
                        allowed_extensions=["pdf"]
                    ), 
                    icon_color=ft.colors.GREY_600,
                    color=ft.colors.GREY_600,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=5)
                    ), 
                ),                                 
            ],
            width=300,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=30,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        expand=True,
        width=500,
        alignment=ft.alignment.center
    )

    page.add(container)

ft.app(target=main, assets_dir="assets")