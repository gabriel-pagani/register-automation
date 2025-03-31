from pyautogui import write, press, click, hotkey
from src.core.commands import smart_click, smart_press
from src.utils.formatter import data_extractor, data_formatter
from time import sleep
from pyperclip import copy
from logging import error
from os import listdir, path, remove
from src.utils.connection import server_request, close_connection


class Register:
    def __init__(self, data: dict, code: str, enrollment: str) -> None:
        self.data = data
        self.code = code
        self.enrollment = enrollment

    def start_registration(self):
        if self.data['situacao'].upper() == 'ATIVA':
            # Abrir o menu de cadastro
            smart_click(r'assets\images\botao_incluir_cadastro.png',
                        flag_path=r'assets\images\filtrar.png')
            smart_press(
                r'assets\images\botao_clientes_fornecedores.png', 'tab')
            sleep(3)

            # Preencher o menu de cadastro
            write(self.code)

            press('tab', presses=2)
            write(self.data['nome fantasia'])

            press('tab')
            write(self.data['nome empresarial'])

            if 'C' in self.code.upper():
                click(x=741, y=412)
            elif 'F' in self.code.upper():
                click(x=741, y=430)
            else:
                return None

            click(x=948, y=441)

            press('tab')
            write(self.data['cnpj'])

            if self.enrollment != '':
                press('tab', presses=3)
                if self.enrollment.isdigit():
                    write(str(self.enrollment))
                click(x=542, y=483)
                click(x=751, y=622)
                if 'I' in self.enrollment.upper():
                    click(x=750, y=651)
                else:
                    click(x=750, y=637)

                click(x=546, y=274)

            click(x=712, y=631)
            write(self.data['cep'])
            press('tab')

            sleep(3)
            click(x=1373, y=736)

            press('tab')
            write(self.data['tipo rua'])
            press('tab', presses=2)
            write(self.data['nome rua'])

            press('tab')
            write(self.data['numero'])

            press('tab', presses=3)
            write(self.data['complemento'])

            press('tab')
            write(self.data['tipo bairro'])
            press('tab', presses=2)
            write(self.data['nome bairro'])

            press('tab', presses=4)
            write(self.data['uf'])

            if self.data['municipio'].isdigit():
                click(x=955, y=711)
            else:
                click(x=1175, y=710)
            copy(self.data['municipio'])
            hotkey('ctrl', 'v')

            click(x=807, y=768)
            write(self.data['celular1'])

            press('tab')
            write(self.data['celular2'])

            press('tab', presses=3)
            write(self.data['email'])

            click(x=1230, y=879)

        else:
            return None

    def check_folder(self):
        try:
            while True:
                response = server_request(
                    query="""
                            SELECT
                                (SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'F%' and CODCOLIGADA = 5 ORDER BY DATACRIACAO DESC, CODCFO DESC) AS COD_FOR,
                                (SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'C%' and CODCOLIGADA = 5 ORDER BY DATACRIACAO DESC, CODCFO DESC) AS COD_CLI;
                        """
                )

                path_docs = r'C:\Users\gabriel.souza\Documents\automacao-de-cadastro\assets\docs'
                diretorio = listdir(path_docs)

                # Verifica se há arquivos PDF
                for arquivo in diretorio:
                    if arquivo.lower().endswith('.pdf') and (arquivo.upper().startswith('C') or arquivo.upper().startswith('F')):

                        caminho_completo = path.join(path_docs, arquivo)

                        # Analisa o PDF e extrai os dados
                        dados = data_formatter(
                            data_extractor(caminho_completo))
                        # Recebe a inscrição estadual
                        inscricao_estadual = arquivo.replace(
                            '.pdf', '').replace('C', '').replace('F', '')
                        if 'X' in inscricao_estadual.upper():
                            inscricao_estadual = ''

                        # Realiza o cadastro usando o Robo
                        if 'F' in arquivo.upper().replace('.PDF', ''):
                            self.code = response['data'][0]['COD_FOR']
                            self.enrollment = inscricao_estadual
                            self.data = dados
                            self.start_registration()

                        elif 'C' in arquivo.upper().replace('.PDF', ''):
                            self.code = response['data'][0]['COD_CLI']
                            self.enrollment = inscricao_estadual
                            self.data = dados
                            self.start_registration()

                        remove(caminho_completo)

                close_connection()

        except Exception as e:
            return None
