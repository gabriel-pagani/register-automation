from pyautogui import click, press, locateOnScreen, position, write, ImageNotFoundException, PAUSE
from re import search, sub, escape
from os import listdir, remove, path
from time import sleep
from fitz import open
from Abreviacoes import abreviacoes

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
    texto_cap = texto.title()

    for key, value in abrv.items():
        # Usar regex para garantir que apenas palavras inteiras sejam substituídas
        texto_cap = sub(r'\b{}\b'.format(escape(key)), value, texto_cap)
            
    # Remove números da string
    texto_cap = sub(r'\b\d+\b', '', texto_cap)

    return texto_cap.strip()

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

def Formatador_De_Dados(dados_extraidos):
    
    dados_formatados = {}
    
    # Nome Empresarial
    dados_formatados['Nome Empresarial'] = Formatador_De_Nome(dados_extraidos['Nome Empresarial']).strip()
    
    # Nome Fantasia
    if '*' in dados_extraidos['Nome Fantasia'] or dados_extraidos['Nome Fantasia'] == dados_extraidos['Nome Empresarial']:
        dados_formatados['Nome Fantasia'] = dados_formatados['Nome Empresarial'].replace('Ltda', '').replace('Sa', '').strip()  
    else:
        dados_formatados['Nome Fantasia'] = Formatador_De_Nome(dados_extraidos['Nome Fantasia'])
  
    # CNPJ
    dados_formatados['Cnpj'] = dados_extraidos['Cnpj'].strip()
    
    # Cep
    dados_formatados['Cep'] = dados_extraidos['Cep'].replace('-', '').replace('.', '').strip()
    
    # Tipo Rua
    dados_formatados['Tipo Rua'] = Formatador_Da_Rua(dados_extraidos['Logradouro'])[0]
    
    # Nome da Rua
    dados_formatados['Nome Rua'] = Formatador_Da_Rua(dados_extraidos['Logradouro'])[1].title()
    
    # Número 
    if not search(r'\d', dados_extraidos['Numero']):
        dados_formatados['Numero'] = ''
    else:
        dados_formatados['Numero'] = dados_extraidos['Numero'].upper().strip()

    # Complemento
    if '*' in dados_extraidos['Complemento']:
        dados_formatados['Complemento'] = ''
    else:
        dados_formatados['Complemento'] = dados_extraidos['Complemento'].title().strip()
    
    # Tipo Bairro
    dados_formatados['Tipo Bairro'] = Formatador_De_Bairro(dados_extraidos['Bairro'])[0]
    
    # Nome do Bairro
    dados_formatados['Nome Bairro'] = Formatador_De_Bairro(dados_extraidos['Bairro'])[1].title()
    
    # Uf
    dados_formatados['Uf'] = dados_extraidos['Uf'].upper().strip()
    
    # Municipio
    dados_formatados['Municipio'] = dados_extraidos['Municipio'].title().strip()
    
    # Celular
    telefone = dados_extraidos['Telefone'].replace('(', '').replace(')', '').replace('-', '').replace(' ', '').strip()
    dados_formatados['Celular1'] = telefone
    dados_formatados['Celular2'] = ''
    if '/' in telefone:
        dados_formatados['Celular1'], dados_formatados['Celular2'] = telefone.split('/')
    if all(char == '0' for char in dados_formatados['Celular2']):
        dados_formatados['Celular2'] = ''
    if dados_formatados['Celular2'] == dados_formatados['Celular1']:
        dados_formatados['Celular2'] = ''

    # Email
    if not '@' in dados_extraidos['Email']:
        dados_formatados['Email'] = ''
    else:
        dados_formatados['Email'] = dados_extraidos['Email'].strip()

    return dados_formatados

def Robo(dados_formatados, Clifor, Insc_est, Output, Autosave):                    
    # Segundo testes o tempo médio para fazer um cadastro é de 17s

    # Velocidade que o programa executa        
    PAUSE = 0.5

    # Espera a menu inicial do RM
    while True:
        try:
            if locateOnScreen(r'C:\AUTOMACAO\Imagens\1.png', confidence=0.95):
                sleep(0.3)
                # Abrir aba de clientes/fornecedores
                click(x=797, y=71)
                break 
        except ImageNotFoundException:
            Output.value += "Abra a Tela de Início do RM!\n"
            Output.update()
            sleep(1)

    # Espera a filtro abrir
    while True:
        try:
            if locateOnScreen(r'C:\AUTOMACAO\Imagens\2.png', confidence=0.9):
                sleep(0.3)
                # Fecha o filtro
                click(x=1123, y=771)
                break 
        except ImageNotFoundException:
            Output.value += "Aguardando menu de Filtros Abrir!\n"
            Output.update()
            sleep(1)

    # Espera a aba de clientes/fornecedores
    while True:
        try:
            if locateOnScreen(r'C:\AUTOMACAO\Imagens\3.png', confidence=0.9):
                sleep(0.3)
                # Abrir cadastro
                click(x=13, y=198)
                break 
        except ImageNotFoundException:
            Output.value += "Aguardado Menu de Clientes/Fornecedores abrir!\n"
            Output.update()
            sleep(1)

    # Espera abrir o menu de cadastro
    while True:
        try:
            if locateOnScreen(r'C:\AUTOMACAO\Imagens\4.png', confidence=0.9):
                sleep(0.3)
                # Escreve o código fornecedor/cliente
                press('tab')
                write(Clifor)
                break 
        except ImageNotFoundException:
            Output.value += "Aguardando Menu de Cadastros Abrir!\n"
            Output.update()
            sleep(1)

    # Escreve o nome fantasia
    press('tab', presses=2)
    write(dados_formatados['Nome Fantasia'])

    # Escreve o nome empresarial
    press('tab')
    write(dados_formatados['Nome Empresarial'])
    
    # Seleciona a clasificação e Categoria
    if 'C' in Clifor.upper(): 
        click(x=710, y=415) # Cliente    
    
    if 'F' in Clifor.upper():
        click(x=709, y=427) # Fornecedor

    click(x=908, y=440) # Jurídica

    # Escreve o CPF/CNPJ
    press('tab')
    write(dados_formatados['Cnpj'])

    # Escreve a inscrição estadual se não for vazio
    if Insc_est != '':
        press('tab', presses=3)
        if Insc_est.isdigit():
            write(str(Insc_est))
        click(x=537, y=489)
        click(x=735, y=619)
        if 'ISENTO' in Insc_est.upper():
            click(x=746, y=652)
        else:
            click(x=739, y=639)  
        click(x=535, y=275)

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
    click(x=1175, y=710)
    write(dados_formatados['Municipio'])
    click(x=807, y=768)

    # Escreve o telefone
    write(dados_formatados['Celular1'])
    press('tab')

    # Escreve o celular
    write(dados_formatados['Celular2'])
    press('tab', presses=3)

    # Escreve o e-mail
    write(dados_formatados['Email'])

    if Autosave:
        # Salva o cadastro
        click(x=1230, y=884)

    # Espera o cadastro terminar
    while True:
        try:
            if locateOnScreen(r'C:\AUTOMACAO\Imagens\5.png', confidence=0.9):
                sleep(0.3)
                # Fecha a aba de fornecedor/cliente
                click(x=176, y=168)
                break 
        except ImageNotFoundException:
            Output.value += "Aguardando o Fechamento da aba de fornecedor/cliente!\n"
            Output.update()
            sleep(1)

def Verificar_Diretorio(Forn, Clie, Output, ForText, CliText, Autosave):

    cod_for = Forn
    cod_cli = Clie   
    tempo_decorrido = 0
    autosave = Autosave

    while True:
        Output.value = f'Procurando arquivos... (Tempo Decorrido: {tempo_decorrido}s)\n'
        Output.update()
        tempo_decorrido += 1
        
        # Lista todos os arquivos no diretório
        caminho_pasta = r'C:\AUTOMACAO\Clifor'
        diretorio = listdir(r"C:\AUTOMACAO\Clifor")
        
        # Verifica se há arquivos PDF
        for arquivo in diretorio:
            
            if arquivo.endswith('.pdf') and (arquivo.upper().startswith('C') or arquivo.upper().startswith('F')):
                
                caminho_completo = path.join(caminho_pasta, arquivo)
                Output.value += f"PDF encontrado: {arquivo.lower().replace('.pdf', '').upper()}\n"
                Output.update()

                # Analisa o PDF e extrai os dados
                dados = Formatador_De_Dados(Extrator_De_Dados(caminho_completo))
                
                # Recebe a inscrição estadual
                inscricao_estadual = arquivo.replace('.pdf', '').replace('C', '').replace('F', '')
                if 'X' in inscricao_estadual.upper():
                    inscricao_estadual = ''

                # Realiza o cadastro usando o Robo
                if 'F' in arquivo.upper().replace('.PDF', ''):
                    Robo(dados, 'F' + str(cod_for + 1), inscricao_estadual, Output, autosave)
                    cod_for += 1
                    ForText.value = cod_for
                    ForText.update()
                elif 'C' in arquivo.upper().replace('.PDF', ''):
                    Robo(dados, 'C' + str(cod_cli + 1), inscricao_estadual, Output, autosave)
                    cod_cli += 1
                    CliText.value = cod_cli
                    CliText.update()                   
                              
                # Remove o arquivo após o processamento
                remove(caminho_completo)
                Output.value += f"PDF processado: {arquivo.replace('.pdf', '').upper()}\n"
                Output.update()    
                tempo_decorrido = 0        
        sleep(1)
