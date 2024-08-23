# Comando para Criar o Execultável

pyinstaller --onefile .\Códigos\Automação.py .\Códigos\Dicionario.py
--add-data "C:\Users\gabriel.souza\Desktop\AUTOMACAO\Imagens\1.png;imagens"
--add-data "C:\Users\gabriel.souza\Desktop\AUTOMACAO\Imagens\2.png;imagens"
--add-data "C:\Users\gabriel.souza\Desktop\AUTOMACAO\Imagens\3.png;imagens"
--add-data "C:\Users\gabriel.souza\Desktop\AUTOMACAO\Imagens\4.png;imagens"
--add-data "C:\Users\gabriel.souza\Desktop\AUTOMACAO\Imagens\5.png;imagens"

# Comando para Instalar todas os Frameworks Necessários

pip install pyautogui pyscreeze Pillow opencv-python-headless flet
