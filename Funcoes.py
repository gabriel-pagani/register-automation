def Robo(dados_formatados, Clifor, Insc_est, Output, Autosave, Is_running):

    if dados_formatados['Situacao'] != 'ATIVA':
        Output.value = "Situação Cadastral Inválida!\n"
        Output.update()
        return

    # Velocidade que o programa executa
    PAUSE = 0.5

    # Espera a menu inicial do RM
    while Is_running():
        try:
            if locateOnScreen(r'C:\Users\gabriel.souza\AUTOMACAO\Imagens\1.png', confidence=0.95):
                Output.update()
                sleep(0.3)
                # Abrir aba de clientes/fornecedores
                click(x=797, y=71)
                break
        except ImageNotFoundException:
            Output.value = "Abra a Tela de Início do RM!\n"
            Output.update()

    # Espera a filtro abrir
    while Is_running():
        try:
            if locateOnScreen(r'C:\Users\gabriel.souza\AUTOMACAO\Imagens\2.png', confidence=0.9):
                Output.update()
                sleep(0.3)
                # Fecha o filtro
                click(x=1123, y=771)
                break
        except ImageNotFoundException:
            Output.value = "Aguardando menu de Filtros Abrir!\n"
            Output.update()

    # Espera a aba de clientes/fornecedores
    while Is_running():
        try:
            if locateOnScreen(r'C:\Users\gabriel.souza\AUTOMACAO\Imagens\3.png', confidence=0.9):
                Output.update()
                sleep(0.3)
                # Abrir cadastro
                click(x=13, y=198)
                break
        except ImageNotFoundException:
            Output.value = "Aguardado Menu de Clientes/Fornecedores abrir!\n"
            Output.update()

    # Espera abrir o menu de cadastro
    while Is_running():
        try:
            if locateOnScreen(r'C:\Users\gabriel.souza\AUTOMACAO\Imagens\4.png', confidence=0.9):
                Output.update()
                sleep(0.3)
                # Escreve o código fornecedor/cliente
                press('tab')
                write(Clifor)
                break
        except ImageNotFoundException:
            Output.value = "Aguardando Menu de Cadastros Abrir!\n"
            Output.update()

    if Is_running():
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

        if Autosave:
            # Salva o cadastro
            click(x=1230, y=884)
        else:
            Output.value = "Salve ou Cancele o Cadastro!\n"

    # Espera o cadastro terminar
    while Is_running():
        try:
            if locateOnScreen(r'C:\Users\gabriel.souza\AUTOMACAO\Imagens\5.png', confidence=0.9):
                Output.update()
                sleep(0.3)
                # Fecha a aba de fornecedor/cliente
                click(x=114, y=168)
                break
        except ImageNotFoundException:
            Output.value = "Aguardando o Fechamento da aba de fornecedor/cliente!\n"
            Output.update()

    if not Is_running():
        Output.value = "Processo Interrompido!\n"
        Output.update()
        return  # Sai da função imediatamente se parar for solicitado


def Verificar_Diretorio(Forn, Clie, Output, ForText, CliText, Autosave, Is_running):

    try:
        cod_for = Forn
        cod_cli = Clie
        tempo_decorrido = 0
        autosave = Autosave

        while Is_running():
            if tempo_decorrido % 10 == 0:
                Output.value = f'Procurando arquivos... (Tempo Decorrido: {
                    tempo_decorrido:.0f}s)\n'
                Output.update()
            tempo_decorrido += 0.5

            # Lista todos os arquivos no diretório
            caminho_pasta = r'C:\Users\gabriel.souza\AUTOMACAO\Clifor'
            diretorio = listdir(r'C:\Users\gabriel.souza\AUTOMACAO\Clifor')

            # Verifica se há arquivos PDF
            for arquivo in diretorio:

                if arquivo.upper().endswith('.PDF') and (arquivo.upper().startswith('C') or arquivo.upper().startswith('F')) and Is_running() == True:

                    caminho_completo = path.join(caminho_pasta, arquivo)
                    Output.value = f"PDF encontrado: {
                        arquivo.lower().replace('.pdf', '').upper()}\n"
                    Output.update()
                    sleep(2)

                    # Analisa o PDF e extrai os dados
                    dados = Formatador_De_Dados(
                        Extrator_De_Dados(caminho_completo))

                    # Recebe a inscrição estadual
                    inscricao_estadual = arquivo.replace(
                        '.pdf', '').replace('C', '').replace('F', '')
                    if 'X' in inscricao_estadual.upper():
                        inscricao_estadual = ''

                    # Realiza o cadastro usando o Robo
                    if 'F' in arquivo.upper().replace('.PDF', '') and Is_running() == True:
                        Robo(dados, 'F' + str(cod_for + 1),
                             inscricao_estadual, Output, autosave, Is_running)
                        if Is_running() == True:
                            cod_for += 1
                            ForText.value = 'F' + str(cod_for)
                            ForText.update()
                    elif 'C' in arquivo.upper().replace('.PDF', '') and Is_running() == True:
                        Robo(dados, 'C' + str(cod_cli + 1),
                             inscricao_estadual, Output, autosave, Is_running)
                        if Is_running() == True:
                            cod_cli += 1
                            CliText.value = 'C' + str(cod_cli)
                            CliText.update()

                    if Is_running() == True:
                        # Remove o arquivo após o processamento
                        remove(caminho_completo)
                        Output.value = f"PDF processado: {
                            arquivo.replace('.pdf', '').upper()}\n"
                        Output.update()
                        sleep(2)
                        tempo_decorrido = 0

            sleep(0.5)

        # A função termina quando is_running() retorna False
        Output.value = f"Processo Reiniciado!\n"
        Output.update()
    except RuntimeError:
        print("Programa Fechado!")
