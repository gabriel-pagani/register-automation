# Criar o Execultável
pyinstaller --onefile Automação.py Interface.py Dicionario.py
--add-data "Escreva o Caminho Para a Imagem\1.png;imagens"
--add-data "Escreva o Caminho Para a Imagem\2.png;imagens"
--add-data "Escreva o Caminho Para a Imagem\3.png;imagens"
--add-data "Escreva o Caminho Para a Imagem\4.png;imagens"
--add-data "Escreva o Caminho Para a Imagem\5.png;imagens"

# Instalar todas os Frameworks Necessários
pip install pyautogui pyscreeze Pillow opencv-python-headless flet
