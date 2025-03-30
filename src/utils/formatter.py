from re import search, sub, escape, IGNORECASE
from abbreviations import abbreviations
from municipalities import municipalities
from fitz import open


def data_extractor(pdf_path: str) -> dict:
    document = open(pdf_path)
    text = document.load_page(0).get_text()

    patterns = {
        "cnpj": r"NÚMERO DE INSCRIÇÃO\n([^\n]+)",
        "nome empresarial": r"NOME EMPRESARIAL\n([^\n]+)",
        "nome fantasia": r"TÍTULO DO ESTABELECIMENTO \(NOME DE FANTASIA\)\n([^\n]+)",
        "logradouro": r"LOGRADOURO\n([^\n]+)",
        "numero": r"NÚMERO\n([^\n]+)",
        "complemento": r"COMPLEMENTO\n([^\n]+)",
        "cep": r"CEP\n([^\n]+)",
        "bairro": r"BAIRRO/DISTRITO\n([^\n]+)",
        "municipio": r"MUNICÍPIO\n([^\n]+)",
        "uf": r"UF\n([^\n]+)",
        "email": r"ENDEREÇO ELETRÔNICO\n([^\n]+)",
        "telefone": r"TELEFONE\n([^\n]+)",
        "situacao": r"SITUAÇÃO CADASTRAL\n([^\n]+)"
    }

    extracted_data = {}

    for key, pattern in patterns.items():
        data = search(pattern, text)
        if data:
            extracted_data[key] = data.group(1).strip()

    return extracted_data


def name_formatter(name: str) -> str:
    abrv = abbreviations
    name = name.title().strip()
    for key, value in abrv.items():
        name = sub(r'\b{}\b'.format(escape(key)), value, name)
    name = sub(r'\b\d+\b', '', name)

    return name.replace('.', '').replace('-', '').replace(',', '').replace('/', '').replace('&', 'e').replace('  ', ' ')


def municipality_formatter(municipality: str) -> str:
    mun = municipalities
    municipality = municipality.upper()

    for key, value in mun.items():
        if municipality == key:
            municipality = value

    return municipality.title()


def street_formatter(street: str) -> list:
    rua = street.strip().split()
    if rua[0].upper() == 'AV':
        return ['Avenida', sub('AV ', '', street)]
    elif rua[0].upper() == 'ROD':
        return ['Rodovia', sub('ROD ', '', street)]
    elif rua[0].upper() == 'EST':
        return ['Estrada', sub('EST ', '', street)]
    elif rua[0].upper() == 'AL':
        return ['Alameda', sub('AL ', '', street)]
    else:
        return ['Rua', sub('R ', '', street)]
    ...
    # Adicionar mais parâmetros conforme necessário


def neighborhood_formatter(neighborhood: str) -> list:
    bairro = neighborhood.strip().split()
    if bairro[0].upper() == 'JARDIM':
        return ['Jardim', sub('JARDIM ', '', neighborhood)]

    elif bairro[0].upper() == 'VILA':
        return ['Vila', sub('VILA ', '', neighborhood)]

    elif bairro[0].upper() == 'ZONA':
        return ['Zona', sub('ZONA ', '', neighborhood)]

    elif bairro[0].upper() == 'PARQUE':
        return ['Parque', sub('PARQUE ', '', neighborhood)]

    elif bairro[0].upper() == 'RESIDENCIAL':
        return ['Residencial', sub('RESIDENCIAL ', '', neighborhood)]

    elif bairro[0].upper() == 'SITIO':
        return ['Sitio', sub('SITIO ', '', neighborhood)]

    elif bairro[0].upper() == 'NUCLEO':
        return ['Nucleo', sub('NUCLEO ', '', neighborhood)]

    elif bairro[0].upper() == 'LOTEAMENTO':
        return ['Loteamento', sub('LOTEAMENTO ', '', neighborhood)]

    elif bairro[0].upper() == 'HORTO':
        return ['Horto', sub('HORTO ', '', neighborhood)]

    elif bairro[0].upper() == 'GLEBA':
        return ['Gleba', sub('GLEBA ', '', neighborhood)]

    elif bairro[0].upper() == 'FAZENDA':
        return ['Fazenda', sub('FAZENDA ', '', neighborhood)]

    elif bairro[0].upper() == 'DISTRITO':
        return ['Distrito', sub('DISTRITO ', '', neighborhood)]

    elif bairro[0].upper() == 'CONJUNTO':
        return ['Conjunto', sub('CONJUNTO ', '', neighborhood)]

    elif bairro[0].upper() == 'CHACARA':
        return ['Chacara', sub('CHACARA ', '', neighborhood)]

    elif bairro[0].upper() == 'BOSQUE':
        return ['Bosque', sub('BOSQUE ', '', neighborhood)]

    elif bairro[0].upper() == 'SRV':
        return ['Servidao', sub('SRV ', '', neighborhood)]

    else:
        return ['Bairro', sub('BAIRRO ', '', neighborhood)]
    ...
    # Adicionar mais parâmetros conforme necessário


def suffix_remover(name: str) -> str:
    name = sub(r'\bLtda\b', '', name, flags=IGNORECASE)
    name = sub(r'\bSa\b', '', name, flags=IGNORECASE)
    return name.strip()


def data_formatter(extracted_data: dict) -> dict:
    formatted_data = {}

    # Nome Empresarial
    formatted_data['nome empresarial'] = name_formatter(
        extracted_data['nome empresarial'])

    # Nome Fantasia
    if '*' in extracted_data['nome fantasia'] or extracted_data['nome fantasia'] == extracted_data['nome empresarial']:
        formatted_data['nome fantasia'] = suffix_remover(
            formatted_data['nome empresarial'])
    else:
        formatted_data['nome fantasia'] = suffix_remover(
            name_formatter(extracted_data['nome fantasia']))

    # CNPJ
    formatted_data['cnpj'] = extracted_data['cnpj'].strip()

    # Cep
    formatted_data['cep'] = extracted_data['cep'].replace(
        '-', '').replace('.', '').strip()

    # Tipo Rua
    formatted_data['tipo rua'] = street_formatter(
        extracted_data['logradouro'])[0]

    # Nome da Rua
    formatted_data['nome rua'] = street_formatter(
        extracted_data['logradouro'])[1].title()

    # Número
    if not search(r'\d', extracted_data['numero']):
        formatted_data['numero'] = ''
    else:
        formatted_data['numero'] = extracted_data['numero'].upper().strip()

    # Complemento
    if '*' in extracted_data['complemento']:
        formatted_data['complemento'] = ''
    else:
        formatted_data['complemento'] = extracted_data['complemento'].title(
        ).strip()

    # Tipo Bairro
    formatted_data['tipo bairro'] = neighborhood_formatter(
        extracted_data['bairro'])[0]

    # Nome do Bairro
    formatted_data['nome bairro'] = neighborhood_formatter(
        extracted_data['bairro'])[1].title()

    # Uf
    formatted_data['uf'] = extracted_data['uf'].upper().strip()

    # Municipio
    formatted_data['municipio'] = municipality_formatter(
        extracted_data['municipio'])

    # Celular
    telefone = extracted_data['telefone'].replace(
        '(', '').replace(')', '').replace('-', '').replace(' ', '').strip()
    formatted_data['celular1'] = telefone
    formatted_data['celular2'] = ''
    if '/' in telefone:
        formatted_data['celular1'], formatted_data['celular2'] = telefone.split(
            '/')
    if all(char == '0' for char in formatted_data['celular2']):
        formatted_data['celular2'] = ''
    if formatted_data['celular2'] == formatted_data['celular1']:
        formatted_data['celular2'] = ''

    # Email
    if not '@' in extracted_data['email']:
        formatted_data['email'] = ''
    else:
        formatted_data['email'] = extracted_data['email'].strip()

    # Situação
    formatted_data['situacao'] = extracted_data['situacao'].strip()

    return formatted_data
