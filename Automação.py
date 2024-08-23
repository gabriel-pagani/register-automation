from pyautogui import click, press, locateOnScreen, position, write, ImageNotFoundException, PAUSE
from re import search, match, sub, escape
from os import listdir, remove, path
from time import sleep
from fitz import open
from Dicionario import abreviacoes

def Input_Codigo_For():
    while True:
        Cli_For = input('Digite o ÚLTIMO código de Fornecedor: ')
        if match(r'^\d{5}$', Cli_For):
            return int(Cli_For)
        print('Código inválido. Tente novamente.')

def Input_Codigo_Cli():
    while True:
        Cli_For = input('Digite o ÚLTIMO código de Cliente: ')
        if match(r'^\d{5}$', Cli_For):
            return int(Cli_For)
        print('Código inválido. Tente novamente.')

def Verificar_Diretorio():

    cod_for = Input_Codigo_For()
    cod_cli = Input_Codigo_Cli()
    tempo_decorrido = 0

    while True:
        print(f'Procurando arquivos... (Tempo Decorrido: {tempo_decorrido}s)')
        tempo_decorrido += 10
        
        # Lista todos os arquivos no diretório
        diretorio_fornecedores = r"C:\Users\gabriel.souza\Desktop\AUTOMACAO\Fornecedores"
        arquivos_fornecedores = listdir(diretorio_fornecedores)
        
        # Verifica se há arquivos PDF
        for arquivo in arquivos_fornecedores:
            if arquivo.endswith('.pdf'):
                caminho_completo = path.join(diretorio_fornecedores, arquivo)
                print(f"PDF encontrado: {arquivo.replace('.pdf', '')}")

                # Analisa o PDF e extrai os dados
                dados_extraidos = Analisador(caminho_completo)
                
                # Recebe a inscrição estadual
                inscricao_estadual = arquivo.replace('.pdf', '')
                if 'X'in inscricao_estadual.upper():
                    inscricao_estadual = ''

                # Realiza o cadastro usando o Robo
                Robo(dados_extraidos, 'F' + str(cod_for + 1), inscricao_estadual)
        
                # Remove ou move o arquivo após o processamento (opcional)
                remove(caminho_completo)
                print(f"PDF processado: {arquivo.replace('.pdf', '')}")
                cod_for += 1
                tempo_decorrido = 0

        diretorio_clientes = r"C:\Users\gabriel.souza\Desktop\AUTOMACAO\Clientes"
        arquivos_clientes = listdir(diretorio_clientes)
        
        # Verifica se há arquivos PDF
        for arquivo in arquivos_clientes:
            if arquivo.endswith('.pdf'):
                caminho_completo = path.join(diretorio_clientes, arquivo)
                print(f"PDF encontrado: {arquivo.replace('.pdf', '')}")

                # Analisa o PDF e extrai os dados
                dados_extraidos = Analisador(caminho_completo)
                
                # Recebe a inscrição estadual
                inscricao_estadual = arquivo.replace('.pdf', '')
                if 'X'in inscricao_estadual.upper():
                    inscricao_estadual = ''

                # Realiza o cadastro usando o Robo
                Robo(dados_extraidos, 'C' + str(cod_cli + 1), inscricao_estadual)
                
                # Remove ou move o arquivo após o processamento (opcional)
                remove(caminho_completo)
                print(f"PDF processado: {arquivo.replace('.pdf', '')}")
                cod_cli += 1
                tempo_decorrido = 0
        
        # Aguardando um tempo antes de verificar novamente
        sleep(10)  # verifica a cada 10 segundos


def Analisador(caminho_pdf):
    documento = open(caminho_pdf)
    texto = documento.load_page(0).get_text()

    padroes = {
        "Número de Inscrição": r"NÚMERO DE INSCRIÇÃO\n([^\n]+)",
        "Nome Empresarial": r"NOME EMPRESARIAL\n([^\n]+)",
        "Nome Fantasia": r"TÍTULO DO ESTABELECIMENTO \(NOME DE FANTASIA\)\n([^\n]+)",
        "Logradouro": r"LOGRADOURO\n([^\n]+)",
        "Número": r"NÚMERO\n([^\n]+)",
        "Complemento": r"COMPLEMENTO\n([^\n]+)",
        "Cep": r"CEP\n([^\n]+)",
        "Bairro/Distrito": r"BAIRRO/DISTRITO\n([^\n]+)",
        "Município": r"MUNICÍPIO\n([^\n]+)",
        "Uf": r"UF\n([^\n]+)",
        "Endereço Eletrônico": r"ENDEREÇO ELETRÔNICO\n([^\n]+)",
        "Telefone": r"TELEFONE\n([^\n]+)",
        "Situação": r"SITUAÇÃO CADASTRAL\n([^\n]+)"
    }

    dados_extraidos = {}
    for chave, padrao in padroes.items():
        correspondencia = search(padrao, texto)
        if correspondencia:
            dados_extraidos[chave] = correspondencia.group(1).strip()

    return dados_extraidos

def Robo(dados, clifor, insc_est):

    cli_for = clifor
    inscricao_estadual = insc_est        
    nome_empresarial = Formatar_Nome(dados["Nome Empresarial"].strip())
    if Formatar_Nome(dados["Nome Fantasia"].strip()) == False:
        nome_fantasia = nome_empresarial.replace('Ltda', '').replace('Sa', '').strip()
    else:
        nome_fantasia = Formatar_Nome(dados["Nome Fantasia"].strip())
    cnpj_cpf = dados['Número de Inscrição'].strip()        
    cep = dados["Cep"].replace('-', '').replace('.', '').strip()
    tipo_rua = Tipo_Rua(dados["Logradouro"].title().strip())[0]
    nome_rua = Tipo_Rua(dados["Logradouro"].title().strip())[1]
    numero = dados["Número"].strip()
    complemento = dados["Complemento"].title().strip()  
    tipo_bairro = Tipo_Bairro(dados["Bairro/Distrito"].title().strip())[0]
    nome_bairro = Tipo_Bairro(dados["Bairro/Distrito"].title().strip())[1]
    uf = dados["Uf"].upper().strip()  
    municipio = dados["Município"].title().strip()                 
    telefone = dados["Telefone"].replace('(', '').replace(')', '').replace('-', '').replace(' ', '').strip()  # Remover formatação do telefone
    celular1 = telefone
    celular2 = ''
    if '/' in telefone:
        celular1, celular2 = telefone.split('/')
    if all(char == '0' for char in celular2):
        celular2 = ''
    if celular2 == celular1:
        celular2 = ''
    email = dados["Endereço Eletrônico"].strip()  
    
    # Velocidade que o programa executa        
    PAUSE = 0.3

    # Espera a menu inicial do RM
    while True:
        try:
            if locateOnScreen(r'C:\Users\gabriel.souza\Desktop\AUTOMACAO\Imagens\1.png', confidence=0.95):
                sleep(0.3)
                # Abrir aba de clientes/fornecedores
                click(x=797, y=71)
                break 
        except ImageNotFoundException:
            print("Abra a Tela de Início do RM!")
            sleep(1)

    # Espera a filtro abrir
    while True:
        try:
            if locateOnScreen(r'C:\Users\gabriel.souza\Desktop\AUTOMACAO\Imagens\2.png', confidence=0.9):
                sleep(0.3)
                # Fecha o filtro
                click(x=1123, y=771)
                break 
        except ImageNotFoundException:
            print("Aguardando menu de Filtros Abrir!")
            sleep(1)

    # Espera a aba de clientes/fornecedores
    while True:
        try:
            if locateOnScreen(r'C:\Users\gabriel.souza\Desktop\AUTOMACAO\Imagens\3.png', confidence=0.9):
                sleep(0.3)
                # Abrir cadastro
                click(x=13, y=198)
                break 
        except ImageNotFoundException:
            print("Aguardado Menu de Clientes/Fornecedores abrir!")
            sleep(1)

    # Espera abrir o menu de cadastro
    while True:
        try:
            if locateOnScreen(r'C:\Users\gabriel.souza\Desktop\AUTOMACAO\Imagens\4.png', confidence=0.9):
                sleep(0.3)
                # Escreve o código fornecedor/cliente
                press('tab')
                write(cli_for)
                break 
        except ImageNotFoundException:
            print("Aguardando Menu de Cadastros Abrir!")
            sleep(1)

    # Escreve o nome fantasia
    if '*' not in nome_fantasia:
        press('tab', presses=2)
        write(nome_fantasia)

    else:
        press('tab', presses=2)
        write(nome_empresarial)

    # Escreve o nome empresarial
    press('tab')
    write(nome_empresarial)
    
    # Seleciona a clasificação e Categoria
    if 'C' in cli_for: 
        click(x=710, y=415) # Cliente    
    
    if 'F' in cli_for:
        click(x=709, y=427) # Fornecedor

    click(x=908, y=440) # Jurídica

    # Escreve o CPF/CNPJ
    press('tab')
    write(cnpj_cpf)

    # Escreve a inscrição estadual se não for vazio
    if inscricao_estadual != '':
        press('tab', presses=3)
        if inscricao_estadual.isdigit():
            write(str(inscricao_estadual))
        click(x=537, y=489)
        click(x=735, y=619)
        if inscricao_estadual.upper() == 'ISENTO':
            click(x=746, y=652)
        else:
            click(x=739, y=639)  
        click(x=535, y=275)

    # Escreve o CEP
    click(x=712, y=631)
    write(str(cep))      
    press('tab')

    # Espera o menu abrir
    sleep(3)

    # Fecha o menu
    click(x=1373, y=736)
    
    # Escreve o tipo e nome da rua       
    click(x=1373, y=736)
    press('tab')
    write(tipo_rua)
    press('tab', presses=2)
    write(nome_rua)
    press('tab')

    # Escreve o número
    if any(char.isdigit() for char in numero):           
        write(numero)
        press('tab', presses=3)
    else:
        press('tab', presses=3)

    # Escreve o complemento
    if '*' not in complemento:
        write(complemento)
        press('tab')
    else:
        press('tab')

    # Escreve o tipo e nome do bairro 
    write(tipo_bairro)
    press('tab', presses=2)
    write(nome_bairro)

    # Escreve a UF
    press('tab', presses=4)
    write(uf)
            
    # Escreve o município
    click(x=1175, y=710)
    write(municipio)
    click(x=807, y=768)

    # Escreve o telefone
    if celular1 != '':
        write(celular1)
        press('tab')
    else:
        press('tab')

    # Escreve o celular
    if celular2 != '':
        write(celular2)
        press('tab', presses=3)
    else:
        press('tab', presses=3)

    # Escreve o e-mail
    if '@' in email:
        write(email)

    # Salva o cadastro
    click(x=1230, y=884)

    # Espera o cadastro terminar
    while True:
        try:
            if locateOnScreen(r'C:\Users\gabriel.souza\Desktop\AUTOMACAO\Imagens\5.png', confidence=0.9):
                sleep(0.3)
                # Fecha a aba de fornecedor/cliente
                click(x=176, y=168)
                break 
        except ImageNotFoundException:
            print("Aguardando o Fechamento da aba de fornecedor/cliente!")
            sleep(1)

def Formatar_Nome(texto):
    # Dicionário com as abreviações conforme o PDF
    abrv = abreviacoes

    if '*' in texto:
        return False

    # Ordena as chaves pelo tamanho para evitar substituições parciais
    abrv = dict(sorted(abrv.items(), key=lambda item: len(item[0]), reverse=True))

    for key, value in abrv.items():
        # Usar regex para garantir que apenas palavras inteiras sejam substituídas
        texto = sub(r'\b{}\b'.format(escape(key)), value, texto)

    for palavra in texto.strip().split():
        if palavra not in abrv.values():
            texto = sub(palavra, palavra.capitalize(), texto)
            
    # Remove números da string
    texto = sub(r'\b\d+\b', '', texto)

    return texto.replace('.', '').replace(',', '').replace('-', '').replace('&', 'e').replace('P/', 'Para').replace('/', '').replace('  ', ' ').strip() 

def Tipo_Rua(texto):
    rua = texto.strip().split()
    if rua[0].upper() == 'AV':
        return ['Avenida', sub('Av ', '', texto)]
    elif rua[0].upper() == 'ROD':
        return ['Rodovia', sub('Rod ', '', texto)]
    elif rua[0].upper() == 'EST':
        return ['Estrada', sub('Est ', '', texto)]
    elif rua[0].upper() == 'AL':
        return ['Alameda', sub('Al ', '', texto)]
    else:
        return ['Rua', sub('R ', '', texto)]
    ...
    # Adicionar mais parâmetros conforme necessário   

def Tipo_Bairro(texto):
    bairro = texto.strip().split()
    if bairro[0].upper() == 'JARDIM' or bairro[0].upper() == 'JDR.':
        return ['Jardim', sub('Jardim ', '', texto)]
    
    elif bairro[0].upper() == 'VILA':
        return ['Vila', sub('Vila ', '', texto)]
    
    elif bairro[0].upper() == 'ZONA':
        return ['Zona', sub('Zona ', '', texto)]
    
    elif bairro[0].upper() == 'PARQUE':
        return ['Parque', sub('Parque ', '', texto)]
    
    elif bairro[0].upper() == 'RESIDENCIAL':
        return ['Residencial', sub('Residencial ', '', texto)]
    
    elif bairro[0].upper() == 'SITIO':
        return ['Sitio', sub('Sitio ', '', texto)]
    
    elif bairro[0].upper() == 'NUCLEO':
        return ['Nucleo', sub('Nucleo ', '', texto)]
    
    elif bairro[0].upper() == 'LOTEAMENTO':
        return ['Loteamento', sub('Loteamento ', '', texto)]
    
    elif bairro[0].upper() == 'HORTO':
        return ['Horto', sub('Horto ', '', texto)]
    
    elif bairro[0].upper() == 'GLEBA':
        return ['Gleba', sub('Gleba ', '', texto)]

    elif bairro[0].upper() == 'FAZENDA':
        return ['Fazenda', sub('Fazenda ', '', texto)]

    elif bairro[0].upper() == 'DISTRITO':
        return ['Distrito', sub('Distrito ', '', texto)]

    elif bairro[0].upper() == 'CONJUNTO':
        return ['Conjunto', sub('Conjunto ', '', texto)]
    
    elif bairro[0].upper() == 'CHACARA':
        return ['Chacara', sub('Chacara ', '', texto)]

    elif bairro[0].upper() == 'BOSQUE':
        return ['Bosque', sub('Bosque ', '', texto)]

    else:
        return ['Bairro', sub('Bairro ', '', texto)]
    ...
    # Adicionar mais parâmetros conforme necessário

Verificar_Diretorio()