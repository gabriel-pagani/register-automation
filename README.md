# Frameworks Necessárias
- pip install pyautogui opencv-python-headless flet PyMuPDF
# Comando Para Criação no Execultável
- pyinstaller --onefile --noconsole --add-data "C:\Seu_Caminho\1.png;imagens" --add-data "C:\Seu_Caminho\2.png;imagens" --add-data "C:\Seu_Caminho\3.png;imagens" --add-data "C:\Seu_Caminho\4.png;imagens" --add-data "C:\Seu_Caminho\5.png;imagens" --icon .\Seu_Caminho\cadastro.ico .\Seu_Caminho\Interface.py .\Seu_Caminho\Funcoes.py .\Seu_Caminho\Abreviacoes.py .\Seu_Caminho\Municipios.py
# Informações Sobre a Automação
- A automação faz cadastro em aproximadamente 17s uma diminuição de aproximadamente 700% do tempo para um feito manualmente
