# Criar o Execultável
pyinstaller --onefile --noconsole 
--add-data "C:\AUTOMACAO\Imagens\1.png;imagens" 
--add-data "C:\AUTOMACAO\Imagens\2.png;imagens" 
--add-data "C:\AUTOMACAO\Imagens\3.png;imagens" 
--add-data "C:\AUTOMACAO\Imagens\4.png;imagens" 
--add-data "C:\AUTOMACAO\Imagens\5.png;imagens" 
--icon "C:\AUTOMACAO\Imagens\Flet.ico" 
Interface.py Funcoes.py Dicionario.py

# Instalar todas os Frameworks Necessários
pip install pyautogui opencv-python-headless flet PyMuPDF 
