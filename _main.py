"""
Sistema de automação para cadastro de clientes/fornecedores a partir de PDF de CNPJ.
Extrai dados de PDFs, formata-os e os insere no sistema RM.
"""

import os
import re
import time
import fitz
import pyautogui
import pyperclip
import base64
from io import BytesIO
from PIL import Image
from src.utils.Abreviacoes import abreviacoes
from src.utils.Municipios import municipios
from src.utils.connection import server_request, close_connection
from src.utils.images_base64 import imagens_base64


class ExtratorDados:
    """Classe para extração e formatação de dados de PDFs de CNPJ."""

    @staticmethod
    def extrair_de_pdf(caminho_pdf):
        """Extrai dados brutos de um PDF de CNPJ."""
        documento = fitz.open(caminho_pdf)
        texto = documento.load_page(0).get_text()

        patterns = {
            "Cnpj": r"NÚMERO DE INSCRIÇÃO\n([^\n]+)",
            "Nome Empresarial": r"NOME EMPRESARIAL\n([^\n]+)",
            "Nome Fantasia": r"TÍTULO DO ESTABELECIMENTO \(NOME DE FANTASIA\)\n([^\n]+)",
            "Logradouro": r"LOGRADOURO\n([^\n]+)",
            "Numero": r"NÚMERO\n([^\n]+)",
            "Complemento": r"COMPLEMENTO\n([^\n]+)",
            "Cep": r"CEP\n([^\n]+)",
            "Bairro": r"BAIRRO/DISTRITO\n([^\n]+)",
            "Municipio": r"MUNICÍPIO\n([^\n]+)",
            "Uf": r"UF\n([^\n]+)",
            "Email": r"ENDEREÇO ELETRÔNICO\n([^\n]+)",
            "Telefone": r"TELEFONE\n([^\n]+)",
            "Situacao": r"SITUAÇÃO CADASTRAL\n([^\n]+)"
        }

        dados_extraidos = {}
        for chave, padrao in patterns.items():
            correspondencia = re.search(padrao, texto)
            if correspondencia:
                dados_extraidos[chave] = correspondencia.group(1).strip()

        return dados_extraidos

    @staticmethod
    def formatar_nome(texto):
        """Formata nomes seguindo padrões específicos."""
        # Converte para title case e remove espaços extras
        texto_cap = texto.title().strip()

        # Aplica abreviações específicas
        for key, value in abreviacoes.items():
            texto_cap = re.sub(r'\b{}\b'.format(
                re.escape(key)), value, texto_cap)

        # Remove números da string
        texto_cap = re.sub(r'\b\d+\b', '', texto_cap)

        # Remove caracteres especiais e normaliza espaços
        return texto_cap.strip().replace('.', '').replace('-', '').replace(',', '') \
            .replace('/', '').replace('&', 'e').replace('  ', ' ')

    @staticmethod
    def formatar_municipio(texto):
        """Formata nomes de municípios conforme dicionário de municípios."""
        texto_cap = texto.upper()

        for key, value in municipios.items():
            if texto_cap == key:
                texto_cap = value

        return texto_cap.strip().title()

    @staticmethod
    def formatar_rua(texto):
        """Identifica e padroniza o tipo de logradouro."""
        rua = texto.strip().split()
        tipo_logradouro = {
            'AV': ['Avenida', re.sub('AV ', '', texto)],
            'ROD': ['Rodovia', re.sub('ROD ', '', texto)],
            'EST': ['Estrada', re.sub('EST ', '', texto)],
            'AL': ['Alameda', re.sub('AL ', '', texto)],
            'R': ['Rua', re.sub('R ', '', texto)]
        }

        if rua[0].upper() in tipo_logradouro:
            return tipo_logradouro[rua[0].upper()]
        else:
            return ['Rua', texto]  # Padrão é Rua

    @staticmethod
    def formatar_bairro(texto):
        """Identifica e padroniza o tipo de bairro."""
        bairro = texto.strip().split()

        tipos_bairro = {
            'JARDIM': 'Jardim',
            'VILA': 'Vila',
            'ZONA': 'Zona',
            'PARQUE': 'Parque',
            'RESIDENCIAL': 'Residencial',
            'SITIO': 'Sitio',
            'NUCLEO': 'Nucleo',
            'LOTEAMENTO': 'Loteamento',
            'HORTO': 'Horto',
            'GLEBA': 'Gleba',
            'FAZENDA': 'Fazenda',
            'DISTRITO': 'Distrito',
            'CONJUNTO': 'Conjunto',
            'CHACARA': 'Chacara',
            'BOSQUE': 'Bosque',
            'SRV': 'Servidao'
        }

        if bairro[0].upper() in tipos_bairro:
            tipo = tipos_bairro[bairro[0].upper()]
            nome = re.sub(f'{bairro[0].upper()} ', '', texto)
            return [tipo, nome]
        else:
            return ['Bairro', re.sub('BAIRRO ', '', texto)]

    @staticmethod
    def remover_sufixos(nome):
        """Remove sufixos comuns de nomes empresariais."""
        nome = re.sub(r'\bLtda\b', '', nome, flags=re.IGNORECASE)
        nome = re.sub(r'\bSa\b', '', nome, flags=re.IGNORECASE)
        return nome.strip()

    @classmethod
    def formatar_dados(cls, dados_extraidos):
        """Formata todos os dados extraídos conforme regras específicas."""
        dados_formatados = {}

        # Nome Empresarial
        dados_formatados['Nome Empresarial'] = cls.formatar_nome(
            dados_extraidos['Nome Empresarial'])

        # Nome Fantasia
        if '*' in dados_extraidos['Nome Fantasia'] or dados_extraidos['Nome Fantasia'] == dados_extraidos['Nome Empresarial']:
            dados_formatados['Nome Fantasia'] = cls.remover_sufixos(
                dados_formatados['Nome Empresarial'])
        else:
            dados_formatados['Nome Fantasia'] = cls.remover_sufixos(
                cls.formatar_nome(dados_extraidos['Nome Fantasia']))

        # CNPJ
        dados_formatados['Cnpj'] = dados_extraidos['Cnpj'].strip()

        # Cep
        dados_formatados['Cep'] = dados_extraidos['Cep'].replace(
            '-', '').replace('.', '').strip()

        # Tipo e Nome da Rua
        rua_info = cls.formatar_rua(dados_extraidos['Logradouro'])
        dados_formatados['Tipo Rua'] = rua_info[0]
        dados_formatados['Nome Rua'] = rua_info[1].title()

        # Número
        if not re.search(r'\d', dados_extraidos['Numero']):
            dados_formatados['Numero'] = ''
        else:
            dados_formatados['Numero'] = dados_extraidos['Numero'].upper(
            ).strip()

        # Complemento
        if '*' in dados_extraidos['Complemento']:
            dados_formatados['Complemento'] = ''
        else:
            dados_formatados['Complemento'] = dados_extraidos['Complemento'].title(
            ).strip()

        # Tipo e Nome do Bairro
        bairro_info = cls.formatar_bairro(dados_extraidos['Bairro'])
        dados_formatados['Tipo Bairro'] = bairro_info[0]
        dados_formatados['Nome Bairro'] = bairro_info[1].title()

        # Uf
        dados_formatados['Uf'] = dados_extraidos['Uf'].upper().strip()

        # Municipio
        dados_formatados['Municipio'] = cls.formatar_municipio(
            dados_extraidos['Municipio'])

        # Celular
        telefone = dados_extraidos['Telefone'].replace(
            '(', '').replace(')', '').replace('-', '').replace(' ', '').strip()

        dados_formatados['Celular1'] = telefone
        dados_formatados['Celular2'] = ''

        if '/' in telefone:
            dados_formatados['Celular1'], dados_formatados['Celular2'] = telefone.split(
                '/')

        if dados_formatados['Celular2'] and all(char == '0' for char in dados_formatados['Celular2']):
            dados_formatados['Celular2'] = ''

        if dados_formatados['Celular2'] == dados_formatados['Celular1']:
            dados_formatados['Celular2'] = ''

        # Email
        dados_formatados['Email'] = '' if '@' not in dados_extraidos['Email'] else dados_extraidos['Email'].strip()

        # Situação
        dados_formatados['Situacao'] = dados_extraidos['Situacao'].strip()

        return dados_formatados


class RoboAutomacao:
    """Classe para realizar automação de cadastro no sistema RM."""

    # Configuração da velocidade de execução
    PAUSA_PADRAO = 0.3

    def __init__(self):
        """Inicializa o robô com configurações padrão."""
        pyautogui.PAUSE = self.PAUSA_PADRAO

    @staticmethod
    def load_image(name_imagem):
        # Obtém a string Base64 da imagem
        base64_string = imagens_base64.get(name_imagem)
        if base64_string:
            # Decodifica a string Base64
            image_data = base64.b64decode(base64_string)
            # Cria uma imagem a partir dos dados decodificados
            return Image.open(BytesIO(image_data))
        else:
            raise ValueError(f"Imagem '{name_imagem}' não encontrada.")

    @staticmethod
    def smart_click(image_path: str, flag_path: str = None):
        while True:
            try:
                if flag_path:
                    if pyautogui.locateOnScreen(flag_path):
                        pyautogui.click(image_path)
                        break
                else:
                    pyautogui.click(image_path)
                    break
            except pyautogui.ImageNotFoundException:
                print('Botão não foi encontrado!')
            time.sleep(0.5)

    @staticmethod
    def smart_click_position(x: int, y: int, flag_path: str):
        while True:
            try:
                if pyautogui.locateOnScreen(flag_path):
                    pyautogui.click(x=x, y=y)
                    break

            except pyautogui.ImageNotFoundException:
                print('Referência não foi encontrada!')
            time.sleep(0.5)

    @staticmethod
    def smart_press(image_path: str, key: str):
        while True:
            try:
                if pyautogui.locateOnScreen(image_path):
                    pyautogui.press(key)
                break
            except pyautogui.ImageNotFoundException:
                print('Referência não foi encontrada!')
            time.sleep(0.5)

    def cadastrar(self, dados_formatados, clifor, insc_est):
        """Realiza o cadastro no sistema RM usando PyAutoGUI."""
        # Verifica se o cadastro está ativo antes de prosseguir
        if dados_formatados['Situacao'] != 'ATIVA':
            return

        # Abre o menu inicial do RM e navega até cadastro
        self.smart_click(
            image_path=r'C:\Users\gabriel.souza\Documents\automacao-de-cadastro\assets\images\clientes_fornecedores.png')

        self.smart_click(
            image_path=r'C:\Users\gabriel.souza\Documents\automacao-de-cadastro\assets\images\fechar.png')

        pyautogui.hotkey('ctrl', 'insert')

        self.smart_press(
            image_path=r'C:\Users\gabriel.souza\Documents\automacao-de-cadastro\assets\images\cadastro_aberto.png', key='tab')
        pyautogui.write(clifor)  # Escreve o código fornecedor/cliente

        # Preenche os dados do cadastro
        pyautogui.press('tab', presses=2)
        pyautogui.write(dados_formatados['Nome Fantasia'].strip())

        pyautogui.press('tab')
        pyautogui.write(dados_formatados['Nome Empresarial'].strip())

        # Seleciona a classificação e Categoria
        if 'C' in clifor.upper():
            pyautogui.click(x=710, y=415)  # Cliente

        if 'F' in clifor.upper():
            pyautogui.click(x=709, y=427)  # Fornecedor

        pyautogui.click(x=908, y=440)  # Jurídica

        # Escreve o CPF/CNPJ
        pyautogui.press('tab')
        pyautogui.write(dados_formatados['Cnpj'])

        # Tratamento da inscrição estadual
        if insc_est:
            pyautogui.press('tab', presses=3)
            if insc_est.isdigit():
                pyautogui.write(str(insc_est))
            pyautogui.click(x=542, y=522)
            pyautogui.click(x=751, y=622)

            if 'I' in insc_est.upper():
                pyautogui.click(x=750, y=651)
            else:
                pyautogui.click(x=750, y=637)

            pyautogui.click(x=546, y=274)

        # Preenche dados de endereço
        pyautogui.click(x=712, y=631)
        pyautogui.write(dados_formatados['Cep'])
        pyautogui.press('tab')

        time.sleep(3)  # Espera o sistema processar o CEP

        pyautogui.click(x=1373, y=736)  # Fecha o menu
        pyautogui.click(x=1373, y=736)

        # Preenche logradouro
        pyautogui.press('tab')
        pyautogui.write(dados_formatados['Tipo Rua'])
        pyautogui.press('tab', presses=2)
        pyautogui.write(dados_formatados['Nome Rua'])
        pyautogui.press('tab')

        # Número e complemento
        pyautogui.write(dados_formatados['Numero'])
        pyautogui.press('tab', presses=3)
        pyautogui.write(dados_formatados['Complemento'])
        pyautogui.press('tab')

        # Bairro
        pyautogui.write(dados_formatados['Tipo Bairro'])
        pyautogui.press('tab', presses=2)
        pyautogui.write(dados_formatados['Nome Bairro'])

        # UF e Município
        pyautogui.press('tab', presses=4)
        pyautogui.write(dados_formatados['Uf'])

        if dados_formatados['Municipio'].isdigit():
            pyautogui.click(x=955, y=711)
        else:
            pyautogui.click(x=1175, y=710)

        pyperclip.copy(dados_formatados['Municipio'])
        pyautogui.hotkey('ctrl', 'v')

        # Contatos
        pyautogui.click(x=807, y=768)
        pyautogui.write(dados_formatados['Celular1'])
        pyautogui.press('tab')

        pyautogui.write(dados_formatados['Celular2'])
        pyautogui.press('tab', presses=3)

        pyautogui.write(dados_formatados['Email'])

        # Salva o cadastro
        pyautogui.click(x=1230, y=884)

        # Espera o cadastro terminar e fecha a aba
        self.smart_click_position(
            flag_path=r'C:\Users\gabriel.souza\Documents\automacao-de-cadastro\assets\images\flag_filtro.png', x=114, y=168)


class ProcessadorDocumentos:
    """Classe para monitorar e processar documentos PDF."""

    CAMINHO_PASTA = r'C:\Users\gabriel.souza\Documents\automacao-de-cadastro\assets\docs'

    def __init__(self):
        """Inicializa o processador com classes necessárias."""
        self.extrator = ExtratorDados()
        self.robo = RoboAutomacao()

    def obter_codigos(self):
        """Obtém os próximos códigos para cliente e fornecedor do banco de dados."""
        query = """
            SELECT
                'F' + RIGHT('00000' + CAST((CAST(SUBSTRING((SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'F%' AND CODCOLIGADA = 5 ORDER BY DATACRIACAO DESC, CODCFO DESC), 2, 5) AS INT) + 1) AS VARCHAR), 5) AS COD_FOR,
                'C' + RIGHT('00000' + CAST((CAST(SUBSTRING((SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'C%' AND CODCOLIGADA = 5 ORDER BY DATACRIACAO DESC, CODCFO DESC), 2, 5) AS INT) + 1) AS VARCHAR), 5) AS COD_CLI
        """
        return server_request(query=query)

    def processar_arquivo(self, arquivo, codigos):
        """Processa um arquivo PDF, extrai dados e realiza cadastro."""
        caminho_completo = os.path.join(self.CAMINHO_PASTA, arquivo)

        # Extrai e formata os dados do PDF
        dados_brutos = self.extrator.extrair_de_pdf(caminho_completo)
        dados_formatados = self.extrator.formatar_dados(dados_brutos)

        # Obtém a inscrição estadual do nome do arquivo
        inscricao_estadual = arquivo.replace(
            '.pdf', '').replace('C', '').replace('F', '')
        if 'X' in inscricao_estadual.upper():
            inscricao_estadual = ''

        # Determina o tipo de cadastro (cliente ou fornecedor) e realiza
        if arquivo.upper().startswith('F'):
            self.robo.cadastrar(
                dados_formatados, codigos['COD_FOR'], inscricao_estadual)
        elif arquivo.upper().startswith('C'):
            self.robo.cadastrar(
                dados_formatados, codigos['COD_CLI'], inscricao_estadual)

        # Remove o arquivo após processamento
        os.remove(caminho_completo)

    def monitorar_diretorio(self):
        """Monitora o diretório por novos arquivos PDF para processar."""
        try:
            while True:
                print('Monitorando Diretório...')
                # Lista todos os arquivos do diretório
                arquivos = os.listdir(self.CAMINHO_PASTA)
                if arquivos:
                    print('Arquivos Detectados!')

                # Processa cada arquivo PDF válido
                for arquivo in arquivos:
                    # Obtém os próximos códigos disponíveis
                    codigos = self.obter_codigos()

                    if (arquivo.upper().endswith('.PDF') and
                            (arquivo.upper().startswith('C') or arquivo.upper().startswith('F'))):

                        self.processar_arquivo(arquivo, codigos)
                        close_connection()

                # Pequena pausa para evitar sobrecarga do CPU
                time.sleep(1)

        except Exception as e:
            print(f"Erro ao processar diretório: {e}")


# Função principal para iniciar o sistema
def main():
    """Inicializa e executa o monitoramento do diretório para processamento de PDFs."""
    processador = ProcessadorDocumentos()
    processador.monitorar_diretorio()


if __name__ == "__main__":
    main()
