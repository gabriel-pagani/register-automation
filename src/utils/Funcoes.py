from pyautogui import click, press, locateOnScreen, write, ImageNotFoundException, PAUSE, hotkey
from re import search, sub, escape, IGNORECASE
from os import listdir, remove, path
from time import sleep
from fitz import open
from src.utils.Abreviacoes import abreviacoes
from src.utils.Municipios import municipios
from pyperclip import copy
from src.utils.connection import server_request, close_connection


def Extrator_De_Dados(caminho_pdf):
    documento = open(caminho_pdf)
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
        correspondencia = search(padrao, texto)
        if correspondencia:
            dados_extraidos[chave] = correspondencia.group(1).strip()

    return dados_extraidos


def Formatador_De_Nome(texto):
    # Dicionário com as abreviações conforme o PDF
    abrv = abreviacoes
    texto_cap = texto.title().strip()

    for key, value in abrv.items():
        # Usar regex para garantir que apenas palavras inteiras sejam substituídas
        texto_cap = sub(r'\b{}\b'.format(escape(key)), value, texto_cap)

    # Remove números da string
    texto_cap = sub(r'\b\d+\b', '', texto_cap)

    return texto_cap.strip().replace('.', '').replace('-', '').replace(',', '').replace('/', '').replace('&', 'e').replace('  ', ' ')


def Formatador_De_Municipio(texto):
    mum = municipios
    texto_cap = texto.upper()

    for key, value in mum.items():
        if texto_cap == key:
            texto_cap = value

    return texto_cap.strip().title()


def Formatador_Da_Rua(texto):
    rua = texto.strip().split()
    if rua[0].upper() == 'AV':
        return ['Avenida', sub('AV ', '', texto)]
    elif rua[0].upper() == 'ROD':
        return ['Rodovia', sub('ROD ', '', texto)]
    elif rua[0].upper() == 'EST':
        return ['Estrada', sub('EST ', '', texto)]
    elif rua[0].upper() == 'AL':
        return ['Alameda', sub('AL ', '', texto)]
    else:
        return ['Rua', sub('R ', '', texto)]
    ...
    # Adicionar mais parâmetros conforme necessário


def Formatador_De_Bairro(texto):
    bairro = texto.strip().split()
    if bairro[0].upper() == 'JARDIM':
        return ['Jardim', sub('JARDIM ', '', texto)]

    elif bairro[0].upper() == 'VILA':
        return ['Vila', sub('VILA ', '', texto)]

    elif bairro[0].upper() == 'ZONA':
        return ['Zona', sub('ZONA ', '', texto)]

    elif bairro[0].upper() == 'PARQUE':
        return ['Parque', sub('PARQUE ', '', texto)]

    elif bairro[0].upper() == 'RESIDENCIAL':
        return ['Residencial', sub('RESIDENCIAL ', '', texto)]

    elif bairro[0].upper() == 'SITIO':
        return ['Sitio', sub('SITIO ', '', texto)]

    elif bairro[0].upper() == 'NUCLEO':
        return ['Nucleo', sub('NUCLEO ', '', texto)]

    elif bairro[0].upper() == 'LOTEAMENTO':
        return ['Loteamento', sub('LOTEAMENTO ', '', texto)]

    elif bairro[0].upper() == 'HORTO':
        return ['Horto', sub('HORTO ', '', texto)]

    elif bairro[0].upper() == 'GLEBA':
        return ['Gleba', sub('GLEBA ', '', texto)]

    elif bairro[0].upper() == 'FAZENDA':
        return ['Fazenda', sub('FAZENDA ', '', texto)]

    elif bairro[0].upper() == 'DISTRITO':
        return ['Distrito', sub('DISTRITO ', '', texto)]

    elif bairro[0].upper() == 'CONJUNTO':
        return ['Conjunto', sub('CONJUNTO ', '', texto)]

    elif bairro[0].upper() == 'CHACARA':
        return ['Chacara', sub('CHACARA ', '', texto)]

    elif bairro[0].upper() == 'BOSQUE':
        return ['Bosque', sub('BOSQUE ', '', texto)]

    elif bairro[0].upper() == 'SRV':
        return ['Servidao', sub('SRV ', '', texto)]

    else:
        return ['Bairro', sub('BAIRRO ', '', texto)]
    ...
    # Adicionar mais parâmetros conforme necessário


def remover_sufixos(nome):
    # Substitui "Ltda" e "Sa" apenas se forem palavras inteiras
    nome = sub(r'\bLtda\b', '', nome, flags=IGNORECASE)
    nome = sub(r'\bSa\b', '', nome, flags=IGNORECASE)
    return nome.strip()


def Formatador_De_Dados(dados_extraidos):
    dados_formatados = {}

    # Nome Empresarial
    dados_formatados['Nome Empresarial'] = Formatador_De_Nome(
        dados_extraidos['Nome Empresarial'])

    # Nome Fantasia
    if '*' in dados_extraidos['Nome Fantasia'] or dados_extraidos['Nome Fantasia'] == dados_extraidos['Nome Empresarial']:
        dados_formatados['Nome Fantasia'] = remover_sufixos(
            dados_formatados['Nome Empresarial'])
    else:
        dados_formatados['Nome Fantasia'] = remover_sufixos(
            Formatador_De_Nome(dados_extraidos['Nome Fantasia']))

    # CNPJ
    dados_formatados['Cnpj'] = dados_extraidos['Cnpj'].strip()

    # Cep
    dados_formatados['Cep'] = dados_extraidos['Cep'].replace(
        '-', '').replace('.', '').strip()

    # Tipo Rua
    dados_formatados['Tipo Rua'] = Formatador_Da_Rua(
        dados_extraidos['Logradouro'])[0]

    # Nome da Rua
    dados_formatados['Nome Rua'] = Formatador_Da_Rua(
        dados_extraidos['Logradouro'])[1].title()

    # Número
    if not search(r'\d', dados_extraidos['Numero']):
        dados_formatados['Numero'] = ''
    else:
        dados_formatados['Numero'] = dados_extraidos['Numero'].upper().strip()

    # Complemento
    if '*' in dados_extraidos['Complemento']:
        dados_formatados['Complemento'] = ''
    else:
        dados_formatados['Complemento'] = dados_extraidos['Complemento'].title(
        ).strip()

    # Tipo Bairro
    dados_formatados['Tipo Bairro'] = Formatador_De_Bairro(
        dados_extraidos['Bairro'])[0]

    # Nome do Bairro
    dados_formatados['Nome Bairro'] = Formatador_De_Bairro(
        dados_extraidos['Bairro'])[1].title()

    # Uf
    dados_formatados['Uf'] = dados_extraidos['Uf'].upper().strip()

    # Municipio
    dados_formatados['Municipio'] = Formatador_De_Municipio(
        dados_extraidos['Municipio'])

    # Celular
    telefone = dados_extraidos['Telefone'].replace(
        '(', '').replace(')', '').replace('-', '').replace(' ', '').strip()
    dados_formatados['Celular1'] = telefone
    dados_formatados['Celular2'] = ''
    if '/' in telefone:
        dados_formatados['Celular1'], dados_formatados['Celular2'] = telefone.split(
            '/')
    if all(char == '0' for char in dados_formatados['Celular2']):
        dados_formatados['Celular2'] = ''
    if dados_formatados['Celular2'] == dados_formatados['Celular1']:
        dados_formatados['Celular2'] = ''

    # Email
    if not '@' in dados_extraidos['Email']:
        dados_formatados['Email'] = ''
    else:
        dados_formatados['Email'] = dados_extraidos['Email'].strip()

    # Situação
    dados_formatados['Situacao'] = dados_extraidos['Situacao'].strip()

    return dados_formatados


def Robo(dados_formatados, Clifor, Insc_est, Is_running):

    if dados_formatados['Situacao'] != 'ATIVA':
        return

    # Velocidade que o programa executa
    PAUSE = 0.5

    # Espera a menu inicial do RM
    while Is_running:
        try:
            if locateOnScreen(r'C:\Users\gabriel.souza\AUTOMACAO\Imagens\1.png', confidence=0.95):
                sleep(0.3)
                # Abrir aba de clientes/fornecedores
                click(x=797, y=71)
                break
        except ImageNotFoundException:
            None

    # Espera a filtro abrir
    while Is_running:
        try:
            if locateOnScreen(r'C:\Users\gabriel.souza\AUTOMACAO\Imagens\2.png', confidence=0.9):
                sleep(0.3)
                # Fecha o filtro
                click(x=1123, y=771)
                break
        except ImageNotFoundException:
            None

    # Espera a aba de clientes/fornecedores
    while Is_running:
        try:
            if locateOnScreen(r'C:\Users\gabriel.souza\AUTOMACAO\Imagens\3.png', confidence=0.9):
                sleep(0.3)
                # Abrir cadastro
                click(x=13, y=198)
                break
        except ImageNotFoundException:
            None

    # Espera abrir o menu de cadastro
    while Is_running:
        try:
            if locateOnScreen(r'C:\Users\gabriel.souza\AUTOMACAO\Imagens\4.png', confidence=0.9):
                sleep(0.3)
                # Escreve o código fornecedor/cliente
                press('tab')
                write(Clifor)
                break
        except ImageNotFoundException:
            None

    if Is_running:
        # Escreve o nome fantasia
        press('tab', presses=2)
        write(dados_formatados['Nome Fantasia'].strip())

        # Escreve o nome empresarial
        press('tab')
        write(dados_formatados['Nome Empresarial'].strip())

        # Seleciona a clasificação e Categoria
        if 'C' in Clifor.upper():
            click(x=710, y=415)  # Cliente

        if 'F' in Clifor.upper():
            click(x=709, y=427)  # Fornecedor

        click(x=908, y=440)  # Jurídica

        # Escreve o CPF/CNPJ
        press('tab')
        write(dados_formatados['Cnpj'])

        # Escreve a inscrição estadual se não for vazio
        if Insc_est != '':
            press('tab', presses=3)
            if Insc_est.isdigit():
                write(str(Insc_est))
            click(x=542, y=483)
            # click(x=543, y=456)  # Coligada 10
            click(x=751, y=622)
            if 'I' in Insc_est.upper():
                click(x=750, y=651)
            else:
                click(x=750, y=637)
            click(x=546, y=274)

        # Escreve o CEP
        click(x=712, y=631)
        write(dados_formatados['Cep'])
        press('tab')

        # Espera o menu abrir
        sleep(3)

        # Fecha o menu
        click(x=1373, y=736)

        # Escreve o tipo e nome da rua
        click(x=1373, y=736)
        press('tab')
        write(dados_formatados['Tipo Rua'])
        press('tab', presses=2)
        write(dados_formatados['Nome Rua'])
        press('tab')

        # Escreve o número
        write(dados_formatados['Numero'])
        press('tab', presses=3)

        # Escreve o complemento
        write(dados_formatados['Complemento'])
        press('tab')

        # Escreve o tipo e nome do bairro
        write(dados_formatados['Tipo Bairro'])
        press('tab', presses=2)
        write(dados_formatados['Nome Bairro'])

        # Escreve a UF
        press('tab', presses=4)
        write(dados_formatados['Uf'])

        # Escreve o município
        if dados_formatados['Municipio'].isdigit():
            click(x=955, y=711)
        else:
            click(x=1175, y=710)
        copy(dados_formatados['Municipio'])
        hotkey('ctrl', 'v')

        # Escreve o telefone
        click(x=807, y=768)
        write(dados_formatados['Celular1'])
        press('tab')

        # Escreve o celular
        write(dados_formatados['Celular2'])
        press('tab', presses=3)

        # Escreve o e-mail
        write(dados_formatados['Email'])

        # Salva o cadastro
        click(x=1230, y=884)

    # Espera o cadastro terminar
    while Is_running:
        try:
            if locateOnScreen(r'C:\Users\gabriel.souza\AUTOMACAO\Imagens\5.png', confidence=0.9):
                sleep(0.3)
                # Fecha a aba de fornecedor/cliente
                click(x=114, y=168)
                break
        except ImageNotFoundException as e:
            None

    if not Is_running:
        return  # Sai da função imediatamente se parar for solicitado


def Verificar_Diretorio(Is_running):

    try:
        while Is_running:
            response = server_request(
                query="""
                    SELECT
                        (SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'F%' and CODCOLIGADA = 5 ORDER BY DATACRIACAO DESC, CODCFO DESC) AS COD_FOR,
                        (SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'C%' and CODCOLIGADA = 5 ORDER BY DATACRIACAO DESC, CODCFO DESC) AS COD_CLI
                """
            )

            # Lista todos os arquivos no diretório
            caminho_pasta = r'C:\Users\gabriel.souza\AUTOMACAO\Clifor'
            diretorio = listdir(r'C:\Users\gabriel.souza\AUTOMACAO\Clifor')

            # Verifica se há arquivos PDF
            for arquivo in diretorio:

                if arquivo.upper().endswith('.PDF') and (arquivo.upper().startswith('C') or arquivo.upper().startswith('F')) and Is_running == True:

                    caminho_completo = path.join(caminho_pasta, arquivo)

                    # Analisa o PDF e extrai os dados
                    dados = Formatador_De_Dados(
                        Extrator_De_Dados(caminho_completo))

                    # Recebe a inscrição estadual
                    inscricao_estadual = arquivo.replace(
                        '.pdf', '').replace('C', '').replace('F', '')
                    if 'X' in inscricao_estadual.upper():
                        inscricao_estadual = ''

                    # Realiza o cadastro usando o Robo
                    if 'F' in arquivo.upper().replace('.PDF', '') and Is_running == True:
                        Robo(dados, response['COD_FOR'],
                             inscricao_estadual, Is_running)
                    elif 'C' in arquivo.upper().replace('.PDF', '') and Is_running == True:
                        Robo(dados, response['COD_CLI'],
                             inscricao_estadual, Is_running)

                    if Is_running == True:
                        # Remove o arquivo após o processamento
                        remove(caminho_completo)

    except RuntimeError:
        print("Programa Fechado!")
