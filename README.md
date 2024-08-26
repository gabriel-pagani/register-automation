# Criar o Execultável
pyinstaller --onefile Interface.py Automação.py Dicionario.py
--add-data "Caminho\1.png;imagens"
--add-data "Caminho\2.png;imagens"
--add-data "Caminho\3.png;imagens"
--add-data "Caminho\4.png;imagens"
--add-data "Caminho\5.png;imagens"

# Instalar todas os Frameworks Necessários
pip install pyautogui opencv-python-headless flet PyMuPDF 
