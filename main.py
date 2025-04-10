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
from src.utils.Abreviacoes import abreviacoes
from src.utils.Municipios import municipios
from src.utils.connection import server_request, close_connection


class ExtratorDados:
    """Classe para extração e formatação de dados de PDFs de CNPJ."""

    @staticmethod
    def extrair_de_pdf(caminho_pdf):
        """Extrai dados brutos de um PDF de CNPJ."""
        print(
            f"\033[34m[INFO]\033[m Extraindo dados do PDF: {os.path.basename(caminho_pdf)}")
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
                print(
                    f"\033[33m[EXTRAÍDO]\033[m {chave}: {dados_extraidos[chave]}")
            else:
                print(
                    f"\033[93m[ALERTA]\033[m Campo '{chave}' não encontrado no PDF")
                dados_extraidos[chave] = ""

        return dados_extraidos

    @staticmethod
    def formatar_nome(texto):
        """Formata nomes seguindo padrões específicos."""
        print(f"\033[34m[INFO]\033[m Formatando nome: {texto}")
        # Converte para title case e remove espaços extras
        texto_cap = texto.title().strip()

        # Aplica abreviações específicas
        for key, value in abreviacoes.items():
            texto_cap = re.sub(r'\b{}\b'.format(
                re.escape(key)), value, texto_cap)

        # Remove números da string
        texto_cap = re.sub(r'\b\d+\b', '', texto_cap)

        # Remove caracteres especiais e normaliza espaços
        resultado = texto_cap.strip().replace('.', '').replace('-', '').replace(',', '') \
            .replace('/', '').replace('&', 'e').replace('  ', ' ')
        print(f"\033[34m[INFO]\033[m Nome formatado: {resultado}")
        return resultado

    @staticmethod
    def formatar_municipio(texto):
        """Formata nomes de municípios conforme dicionário de municípios."""
        print(f"\033[34m[INFO]\033[m Formatando município: {texto}")
        texto_cap = texto.upper()

        for key, value in municipios.items():
            if texto_cap == key:
                texto_cap = value
                print(
                    f"\033[34m[INFO]\033[m Encontrada correspondência no dicionário: {value}")
                break

        resultado = texto_cap.strip().title()
        print(f"\033[34m[INFO]\033[m Município formatado: {resultado}")
        return resultado

    @staticmethod
    def formatar_rua(texto):
        """Identifica e padroniza o tipo de logradouro."""
        print(f"\033[34m[INFO]\033[m Formatando logradouro: {texto}")
        rua = texto.strip().split()
        tipo_logradouro = {
            'AV': ['Avenida', re.sub('AV ', '', texto)],
            'ROD': ['Rodovia', re.sub('ROD ', '', texto)],
            'EST': ['Estrada', re.sub('EST ', '', texto)],
            'AL': ['Alameda', re.sub('AL ', '', texto)],
            'R': ['Rua', re.sub('R ', '', texto)]
        }

        if rua[0].upper() in tipo_logradouro:
            print(
                f"\033[34m[INFO]\033[m Tipo de logradouro identificado: {rua[0].upper()} -> {tipo_logradouro[rua[0].upper()][0]}")
            return tipo_logradouro[rua[0].upper()]
        else:
            print(
                f"\033[34m[INFO]\033[m Tipo de logradouro não identificado, usando padrão 'Rua'")
            return ['Rua', texto]  # Padrão é Rua

    @staticmethod
    def formatar_bairro(texto):
        """Identifica e padroniza o tipo de bairro."""
        print(f"\033[34m[INFO]\033[m Formatando bairro: {texto}")
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
            print(
                f"\033[34m[INFO]\033[m Tipo de bairro identificado: {bairro[0].upper()} -> {tipo}")
            return [tipo, nome]
        else:
            print(
                f"\033[34m[INFO]\033[m Tipo de bairro não identificado, usando padrão 'Bairro'")
            return ['Bairro', re.sub('BAIRRO ', '', texto)]

    @staticmethod
    def remover_sufixos(nome):
        """Remove sufixos comuns de nomes empresariais."""
        print(f"\033[34m[INFO]\033[m Removendo sufixos de: {nome}")
        nome = re.sub(r'\bLtda\b', '', nome, flags=re.IGNORECASE)
        nome = re.sub(r'\bSa\b', '', nome, flags=re.IGNORECASE)
        resultado = nome.strip()
        print(
            f"\033[34m[INFO]\033[m Resultado após remoção de sufixos: {resultado}")
        return resultado

    @classmethod
    def formatar_dados(cls, dados_extraidos):
        """Formata todos os dados extraídos conforme regras específicas."""
        print("\n\033[34m[INFO]\033[m Iniciando formatação de dados...")
        dados_formatados = {}

        # Nome Empresarial
        dados_formatados['Nome Empresarial'] = cls.formatar_nome(
            dados_extraidos['Nome Empresarial'])

        # Nome Fantasia
        if '*' in dados_extraidos['Nome Fantasia'] or dados_extraidos['Nome Fantasia'] == dados_extraidos['Nome Empresarial']:
            print(
                "\033[34m[INFO]\033[m Nome fantasia não disponível ou igual ao nome empresarial, usando nome empresarial")
            dados_formatados['Nome Fantasia'] = cls.remover_sufixos(
                dados_formatados['Nome Empresarial'])
        else:
            dados_formatados['Nome Fantasia'] = cls.remover_sufixos(
                cls.formatar_nome(dados_extraidos['Nome Fantasia']))

        # CNPJ
        dados_formatados['Cnpj'] = dados_extraidos['Cnpj'].strip()
        print(
            f"\033[34m[INFO]\033[m CNPJ formatado: {dados_formatados['Cnpj']}")

        # Cep
        dados_formatados['Cep'] = dados_extraidos['Cep'].replace(
            '-', '').replace('.', '').strip()
        print(f"\033[34m[INFO]\033[m CEP formatado: {dados_formatados['Cep']}")

        # Tipo e Nome da Rua
        rua_info = cls.formatar_rua(dados_extraidos['Logradouro'])
        dados_formatados['Tipo Rua'] = rua_info[0]
        dados_formatados['Nome Rua'] = rua_info[1].title()
        print(
            f"\033[34m[INFO]\033[m Rua formatada: {dados_formatados['Tipo Rua']} {dados_formatados['Nome Rua']}")

        # Número
        if not re.search(r'\d', dados_extraidos['Numero']):
            print(
                "\033[34m[INFO]\033[m Número não contém dígitos, definindo como vazio")
            dados_formatados['Numero'] = ''
        else:
            dados_formatados['Numero'] = dados_extraidos['Numero'].upper(
            ).strip()
            print(
                f"\033[34m[INFO]\033[m Número formatado: {dados_formatados['Numero']}")

        # Complemento
        if '*' in dados_extraidos['Complemento']:
            print(
                "\033[34m[INFO]\033[m Complemento não disponível, definindo como vazio")
            dados_formatados['Complemento'] = ''
        else:
            dados_formatados['Complemento'] = dados_extraidos['Complemento'].title(
            ).strip()
            print(
                f"\033[34m[INFO]\033[m Complemento formatado: {dados_formatados['Complemento']}")

        # Tipo e Nome do Bairro
        bairro_info = cls.formatar_bairro(dados_extraidos['Bairro'])
        dados_formatados['Tipo Bairro'] = bairro_info[0]
        dados_formatados['Nome Bairro'] = bairro_info[1].title()
        print(
            f"\033[34m[INFO]\033[m Bairro formatado: {dados_formatados['Tipo Bairro']} {dados_formatados['Nome Bairro']}")

        # Uf
        dados_formatados['Uf'] = dados_extraidos['Uf'].upper().strip()
        print(f"\033[34m[INFO]\033[m UF formatada: {dados_formatados['Uf']}")

        # Municipio
        dados_formatados['Municipio'] = cls.formatar_municipio(
            dados_extraidos['Municipio'])
        print(
            f"\033[34m[INFO]\033[m Município formatado: {dados_formatados['Municipio']}")

        # Celular
        telefone = dados_extraidos['Telefone'].replace(
            '(', '').replace(')', '').replace('-', '').replace(' ', '').strip()
        print(f"\033[34m[INFO]\033[m Telefone extraído: {telefone}")

        dados_formatados['Celular1'] = telefone
        dados_formatados['Celular2'] = ''

        if '/' in telefone:
            dados_formatados['Celular1'], dados_formatados['Celular2'] = telefone.split(
                '/')
            print(
                f"\033[34m[INFO]\033[m Múltiplos telefones detectados: {dados_formatados['Celular1']} e {dados_formatados['Celular2']}")

        if dados_formatados['Celular2'] and all(char == '0' for char in dados_formatados['Celular2']):
            print(
                "\033[34m[INFO]\033[m Celular2 contém apenas zeros, definindo como vazio")
            dados_formatados['Celular2'] = ''

        if dados_formatados['Celular2'] == dados_formatados['Celular1']:
            print(
                "\033[34m[INFO]\033[m Celular2 é igual ao Celular1, definindo Celular2 como vazio")
            dados_formatados['Celular2'] = ''

        # Email
        if '@' not in dados_extraidos['Email']:
            print(
                "\033[34m[INFO]\033[m Email inválido detectado, definindo como vazio")
            dados_formatados['Email'] = ''
        else:
            dados_formatados['Email'] = dados_extraidos['Email'].strip(
            ).lower()
            print(
                f"\033[34m[INFO]\033[m Email formatado: {dados_formatados['Email']}")

        # Situação
        dados_formatados['Situacao'] = dados_extraidos['Situacao'].strip()
        print(f"\033[34m[INFO]\033[m Situação: {dados_formatados['Situacao']}")

        print("\033[34m[INFO]\033[m Formatação de dados concluída!")
        return dados_formatados


class RoboAutomacao:
    """Classe para realizar automação de cadastro no sistema RM."""

    # Configuração da velocidade de execução
    PAUSA_PADRAO = 0.3

    def __init__(self):
        """Inicializa o robô com configurações padrão."""
        print("\033[34m[INFO]\033[m Inicializando robô de automação...")
        pyautogui.PAUSE = self.PAUSA_PADRAO
        print(
            f"\033[35m[CONFIG]\033[m Pausa padrão configurada para {self.PAUSA_PADRAO} segundos")

    @staticmethod
    def smart_click(image_path: str, flag_path: str = None):
        print(
            f"\033[36m[AÇÃO]\033[m Tentando clicar na imagem: {os.path.basename(image_path)}")
        tentativas = 0
        while True:
            tentativas += 1
            try:
                if flag_path:
                    print(
                        f"\033[36m[AÇÃO]\033[m Verificando flag: {os.path.basename(flag_path)}")
                    if pyautogui.locateOnScreen(flag_path, confidence=0.95):
                        print(
                            f"\033[36m[AÇÃO]\033[m Flag encontrada, clicando na imagem")
                        pyautogui.click(image_path)
                        print(
                            f"\033[32m[SUCESSO]\033[m Clique realizado após {tentativas} tentativas")
                        break
                else:
                    pyautogui.click(image_path)
                    print(
                        f"\033[32m[SUCESSO]\033[m Clique realizado após {tentativas} tentativas")
                    break
            except pyautogui.ImageNotFoundException:
                print(
                    f"\033[93m[ALERTA]\033[m Tentativa {tentativas}: Botão não foi encontrado! Aguardando...")
            time.sleep(0.5)

    @staticmethod
    def smart_click_position(x: int, y: int, flag_path: str):
        print(
            f"\033[36m[AÇÃO]\033[m Tentando clicar na posição ({x}, {y}) após detectar flag")
        tentativas = 0
        while True:
            tentativas += 1
            try:
                if pyautogui.locateOnScreen(flag_path, confidence=0.95):
                    print(
                        f"\033[36m[AÇÃO]\033[m Flag encontrada, clicando na posição ({x}, {y})")
                    pyautogui.click(x=x, y=y)
                    print(
                        f"\033[32m[SUCESSO]\033[m Clique na posição realizado após {tentativas} tentativas")
                    break

            except pyautogui.ImageNotFoundException:
                print(
                    f"\033[93m[ALERTA]\033[m Tentativa {tentativas}: Referência não foi encontrada! Aguardando...")
            time.sleep(0.5)

    @staticmethod
    def smart_press(image_path: str, key: str):
        print(
            f"\033[36m[AÇÃO]\033[m Tentando pressionar a tecla '{key}' após detectar imagem")
        tentativas = 0
        while True:
            tentativas += 1
            try:
                if pyautogui.locateOnScreen(image_path):
                    print(
                        f"\033[36m[AÇÃO]\033[m Imagem encontrada, pressionando tecla '{key}'")
                    pyautogui.press(key)
                    print(
                        f"\033[32m[SUCESSO]\033[m Tecla pressionada após {tentativas} tentativas")
                break
            except pyautogui.ImageNotFoundException:
                print(
                    f"\033[93m[ALERTA]\033[m Tentativa {tentativas}: Referência não foi encontrada! Aguardando...")
            time.sleep(0.5)

    def cadastrar(self, dados_formatados, clifor, insc_est):
        """Realiza o cadastro no sistema RM usando PyAutoGUI."""
        print(
            f"\n\033[34m[INFO]\033[m Iniciando cadastro no sistema RM para o código {clifor}")

        # Verifica se o cadastro está ativo antes de prosseguir
        if dados_formatados['Situacao'] != 'ATIVA':
            print(
                f"\033[93m[ALERTA]\033[m Situação cadastral não está ATIVA: {dados_formatados['Situacao']}. Abortando cadastro.")
            return

        print("\033[36m[AÇÃO]\033[m Abrindo menu inicial do RM")
        # Abre o menu inicial do RM e navega até cadastro
        self.smart_click(
            image_path=r'\\serverfile\users\Tecnologia\Softwares\Windows\register-automation\assets\images\clientes_fornecedores.png')

        print("\033[36m[AÇÃO]\033[m Fechando notificações se houver")
        self.smart_click(
            image_path=r'\\serverfile\users\Tecnologia\Softwares\Windows\register-automation\assets\images\fechar.png')

        print("\033[36m[AÇÃO]\033[m Pressionando Ctrl+Insert para novo cadastro")
        pyautogui.hotkey('ctrl', 'insert')
        print("\033[34m[INFO]\033[m Novo formulário de cadastro aberto")

        print("\033[36m[AÇÃO]\033[m Posicionando cursor no campo de código")
        self.smart_press(
            image_path=r'\\serverfile\users\Tecnologia\Softwares\Windows\register-automation\assets\images\cadastro_aberto.png', key='tab')
        print(f"\033[36m[AÇÃO]\033[m Digitando código: {clifor}")
        pyautogui.write(clifor)  # Escreve o código fornecedor/cliente

        # Preenche os dados do cadastro
        print("\033[36m[AÇÃO]\033[m Preenchendo Nome Fantasia")
        pyautogui.press('tab', presses=2)
        print(
            f"\033[95m[VALOR]\033[m Nome Fantasia: {dados_formatados['Nome Fantasia'].strip()}")
        pyautogui.write(dados_formatados['Nome Fantasia'].strip())

        print("\033[36m[AÇÃO]\033[m Preenchendo Nome Empresarial")
        pyautogui.press('tab')
        print(
            f"\033[95m[VALOR]\033[m Nome Empresarial: {dados_formatados['Nome Empresarial'].strip()}")
        pyautogui.write(dados_formatados['Nome Empresarial'].strip())

        # Seleciona a classificação e Categoria
        if 'C' in clifor.upper():
            print("\033[36m[AÇÃO]\033[m Selecionando classificação: Cliente")
            pyautogui.click(x=710, y=415)  # Cliente

        if 'F' in clifor.upper():
            print("\033[36m[AÇÃO]\033[m Selecionando classificação: Fornecedor")
            pyautogui.click(x=709, y=427)  # Fornecedor

        print("\033[36m[AÇÃO]\033[m Selecionando categoria: Jurídica")
        pyautogui.click(x=908, y=440)  # Jurídica

        # Escreve o CPF/CNPJ
        print("\033[36m[AÇÃO]\033[m Preenchendo CNPJ")
        pyautogui.press('tab')
        print(f"\033[95m[VALOR]\033[m CNPJ: {dados_formatados['Cnpj']}")
        pyautogui.write(dados_formatados['Cnpj'])

        # Tratamento da inscrição estadual
        if insc_est:
            print(
                f"\033[34m[INFO]\033[m Processando inscrição estadual: {insc_est}")
            pyautogui.press('tab', presses=3)
            if insc_est.isdigit():
                print(
                    "\033[36m[AÇÃO]\033[m Digitando inscrição estadual numérica")
                pyautogui.write(str(insc_est))
            print(
                "\033[36m[AÇÃO]\033[m Clicando para configurar inscrição estadual")
            pyautogui.click(x=542, y=522)
            pyautogui.click(x=751, y=622)

            if 'I' in insc_est.upper():
                print(
                    "\033[36m[AÇÃO]\033[m Selecionando ISENTO para inscrição estadual")
                pyautogui.click(x=750, y=651)
            else:
                print(
                    "\033[36m[AÇÃO]\033[m Selecionando opção padrão para inscrição estadual")
                pyautogui.click(x=750, y=637)

            print("\033[36m[AÇÃO]\033[m Fechando menu de inscrição estadual")
            pyautogui.click(x=546, y=274)

        # Preenche dados de endereço
        print("\033[36m[AÇÃO]\033[m Preenchendo CEP")
        pyautogui.click(x=712, y=631)
        print(f"\033[95m[VALOR]\033[m CEP: {dados_formatados['Cep']}")
        pyautogui.write(dados_formatados['Cep'])
        pyautogui.press('tab')

        print(
            "\033[34m[INFO]\033[m Aguardando sistema processar o CEP (3 segundos)")
        time.sleep(3)  # Espera o sistema processar o CEP

        print("\033[36m[AÇÃO]\033[m Fechando menus pop-up se houver")
        pyautogui.click(x=1373, y=736)  # Fecha o menu
        pyautogui.click(x=1373, y=736)

        # Preenche logradouro
        print("\033[36m[AÇÃO]\033[m Preenchendo dados de logradouro")
        pyautogui.press('tab')
        print(
            f"\033[95m[VALOR]\033[m Tipo Rua: {dados_formatados['Tipo Rua']}")
        pyautogui.write(dados_formatados['Tipo Rua'])
        pyautogui.press('tab', presses=2)
        print(
            f"\033[95m[VALOR]\033[m Nome Rua: {dados_formatados['Nome Rua']}")
        pyautogui.write(dados_formatados['Nome Rua'])
        pyautogui.press('tab')

        # Número e complemento
        print("\033[36m[AÇÃO]\033[m Preenchendo número")
        print(f"\033[95m[VALOR]\033[m Número: {dados_formatados['Numero']}")
        pyautogui.write(dados_formatados['Numero'])
        pyautogui.press('tab', presses=3)
        print("\033[36m[AÇÃO]\033[m Preenchendo complemento")
        print(
            f"\033[95m[VALOR]\033[m Complemento: {dados_formatados['Complemento']}")
        pyautogui.write(dados_formatados['Complemento'])
        pyautogui.press('tab')

        # Bairro
        print("\033[36m[AÇÃO]\033[m Preenchendo dados do bairro")
        print(
            f"\033[95m[VALOR]\033[m Tipo Bairro: {dados_formatados['Tipo Bairro']}")
        pyautogui.write(dados_formatados['Tipo Bairro'])
        pyautogui.press('tab', presses=2)
        print(
            f"\033[95m[VALOR]\033[m Nome Bairro: {dados_formatados['Nome Bairro']}")
        pyautogui.write(dados_formatados['Nome Bairro'])

        # UF e Município
        print("\033[36m[AÇÃO]\033[m Preenchendo UF")
        pyautogui.press('tab', presses=4)
        print(f"\033[95m[VALOR]\033[m UF: {dados_formatados['Uf']}")
        pyautogui.write(dados_formatados['Uf'])

        print("\033[36m[AÇÃO]\033[m Preenchendo Município")
        pyautogui.click(x=1175, y=710)
        print(
            f"\033[95m[VALOR]\033[m Município: {dados_formatados['Municipio']}")
        pyperclip.copy(dados_formatados['Municipio'])
        pyautogui.hotkey('ctrl', 'v')

        # Contatos
        print("\033[36m[AÇÃO]\033[m Preenchendo dados de contato")
        pyautogui.click(x=807, y=768)
        print(
            f"\033[95m[VALOR]\033[m Celular1: {dados_formatados['Celular1']}")
        pyautogui.write(dados_formatados['Celular1'])
        pyautogui.press('tab')

        print(
            f"\033[95m[VALOR]\033[m Celular2: {dados_formatados['Celular2']}")
        pyautogui.write(dados_formatados['Celular2'])
        pyautogui.press('tab', presses=3)

        print(f"\033[95m[VALOR]\033[m Email: {dados_formatados['Email']}")
        pyautogui.write(dados_formatados['Email'])

        # Salva o cadastro
        print("\033[36m[AÇÃO]\033[m Salvando cadastro")
        pyautogui.click(x=1230, y=884)
        print("\033[34m[INFO]\033[m Comando de salvar enviado")

        # Espera o cadastro terminar e fecha a aba
        print(
            "\033[36m[AÇÃO]\033[m Aguardando finalização do cadastro e fechando aba")
        self.smart_click_position(
            flag_path=r'\\serverfile\users\Tecnologia\Softwares\Windows\register-automation\assets\images\flag_filtro.png', x=114, y=168)
        print(
            f"\033[32m[SUCESSO]\033[m Cadastro de {clifor} finalizado com sucesso!")


class ProcessadorDocumentos:
    """Classe para monitorar e processar documentos PDF."""

    CAMINHO_PASTA = r'\\serverfile\users\Tecnologia\Softwares\Windows\register-automation\assets\docs'

    def __init__(self):
        """Inicializa o processador com classes necessárias."""
        print("\033[34m[INFO]\033[m Inicializando Processador de Documentos")
        self.extrator = ExtratorDados()
        self.robo = RoboAutomacao()
        print(f"\033[35m[CONFIG]\033[m Pasta monitorada: {self.CAMINHO_PASTA}")

    def obter_codigos(self):
        """Obtém os próximos códigos para cliente e fornecedor do banco de dados."""
        print(
            "\033[34m[INFO]\033[m Obtendo próximos códigos disponíveis do banco de dados")
        query = """
            SELECT
                'F' + RIGHT('00000' + CAST((CAST(SUBSTRING((SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'F%' AND CODCOLIGADA = 5 ORDER BY DATACRIACAO DESC, CODCFO DESC), 2, 5) AS INT) + 1) AS VARCHAR), 5) AS COD_FOR,
                'C' + RIGHT('00000' + CAST((CAST(SUBSTRING((SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'C%' AND CODCOLIGADA = 5 ORDER BY DATACRIACAO DESC, CODCFO DESC), 2, 5) AS INT) + 1) AS VARCHAR), 5) AS COD_CLI
        """
        try:
            codigos = server_request(query=query)
            print(
                f"\033[34m[INFO]\033[m Códigos obtidos - Fornecedor: {codigos['COD_FOR']}, Cliente: {codigos['COD_CLI']}")
            return codigos
        except Exception as e:
            print(
                f"\033[31m[ERRO]\033[m Falha ao obter códigos do banco de dados: {e}")
            return None

    def processar_arquivo(self, arquivo, codigos):
        """Processa um arquivo PDF, extrai dados e realiza cadastro."""
        print(
            f"\n\033[34m[INFO]\033[m ==== PROCESSANDO ARQUIVO: {arquivo} ====")
        caminho_completo = os.path.join(self.CAMINHO_PASTA, arquivo)

        # Extrai e formata os dados do PDF
        print("\033[34m[INFO]\033[m Iniciando extração de dados do PDF")
        dados_brutos = self.extrator.extrair_de_pdf(caminho_completo)
        print("\033[34m[INFO]\033[m Iniciando formatação dos dados extraídos")
        dados_formatados = self.extrator.formatar_dados(dados_brutos)

        # Obtém a inscrição estadual do nome do arquivo
        inscricao_estadual = arquivo.replace(
            '.pdf', '').replace('C', '').replace('F', '')
        if 'X' in inscricao_estadual.upper():
            print(
                "\033[34m[INFO]\033[m Inscrição estadual marcada como não aplicável (X)")
            inscricao_estadual = ''
        print(
            f"\033[34m[INFO]\033[m Inscrição Estadual: {inscricao_estadual if inscricao_estadual else 'Não informada'}")

        # Determina o tipo de cadastro (cliente ou fornecedor) e realiza
        if arquivo.upper().startswith('F'):
            print(
                f"\033[34m[INFO]\033[m Tipo de cadastro: FORNECEDOR - Código: {codigos['COD_FOR']}")
            self.robo.cadastrar(
                dados_formatados, codigos['COD_FOR'], inscricao_estadual)
        elif arquivo.upper().startswith('C'):
            print(
                f"\033[34m[INFO]\033[m Tipo de cadastro: CLIENTE - Código: {codigos['COD_CLI']}")
            self.robo.cadastrar(
                dados_formatados, codigos['COD_CLI'], inscricao_estadual)
        else:
            print(
                f"\033[93m[ALERTA]\033[m Prefixo do arquivo não reconhecido: {arquivo} - Não será processado")

        # Remove o arquivo após processamento
        try:
            os.remove(caminho_completo)
            print(
                f"\033[34m[INFO]\033[m Arquivo {arquivo} removido após processamento")
        except Exception as e:
            print(
                f"\033[31m[ERRO]\033[m Não foi possível remover o arquivo {arquivo}: {e}")

    def monitorar_diretorio(self):
        """Monitora o diretório por novos arquivos PDF para processar."""
        print(
            "\n\033[34m[INFO]\033[m ==== INICIANDO MONITORAMENTO DE DIRETÓRIO ====")
        ciclo = 0
        try:
            while True:
                ciclo += 1
                print(
                    f"\n\033[34m[INFO]\033[m Ciclo de monitoramento #{ciclo} - {time.strftime('%H:%M:%S')}")
                # Lista todos os arquivos do diretório
                arquivos = os.listdir(self.CAMINHO_PASTA)
                if arquivos:
                    print(
                        f"\033[34m[INFO]\033[m {len(arquivos)} arquivo(s) detectado(s): {', '.join(arquivos)}")
                else:
                    print(
                        "\033[34m[INFO]\033[m Nenhum arquivo detectado neste ciclo")

                # Processa cada arquivo PDF válido
                arquivos_processados = 0
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
