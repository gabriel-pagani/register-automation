# Frameworks Necessárias
- pip install pyautogui opencv-python-headless flet PyMuPDF pyperclip
# Comando Para Criação no Execultável
- pyinstaller --onefile --noconsole --add-data "C:\Imagens\1.png;imagens" --add-data "C:\Imagens\2.png;imagens" --add-data "C:\Imagens\3.png;imagens" --add-data "C:\Imagens\4.png;imagens" --add-data "C:\Imagens\5.png;imagens" --icon .\Imagens\cadastro.ico .\Códigos\Interface.py .\Códigos\Funcoes.py .\Códigos\Abreviacoes.py .\Códigos\Municipios.py
# Informações Sobre a Automação
- A automação faz cadastro em aproximadamente 15s uma diminuição de aproximadamente 700% do tempo para um feito manualmente
