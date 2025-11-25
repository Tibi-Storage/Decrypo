import string

ALFABETO = string.ascii_uppercase

def normalizar(txt):
    txt = txt.upper()
    return "".join(c for c in txt if c in ALFABETO)


def gerar_tabula_recta():
    tabela = []
    for i in range(26):
        linha = ALFABETO[i:] + ALFABETO[:i]
        tabela.append(linha)
    return tabela


def ler_tabela_vigenere(path):
    if not path:
        return gerar_tabula_recta()
    with open(path, 'r', encoding='utf-8') as f:
        linhas = [l.strip().upper() for l in f if l.strip()]
    if len(linhas) == 26 and all(len(l) >= 26 for l in linhas):
        tabela = [l[:26] for l in linhas]
        return tabela
    texto = ''.join(linhas)
    if len(texto) >= 26*26:
        tabela = [texto[i*26:(i+1)*26] for i in range(26)]
        return tabela
    raise ValueError('Ficheiro de tabela Vigenere inválido: espere 26 linhas de 26 letras')


def cifrar_vigenere(msg, chave, tabela):
    msg = normalizar(msg)
    chave = normalizar(chave)
    if not msg:
        raise ValueError("Mensagem vazia depois de normalizada")
    if not chave:
        raise ValueError("Chave vazia depois de normalizada")
    res = ""
    for i, c in enumerate(msg):
        k = chave[i % len(chave)]
        linha = ALFABETO.index(k)
        coluna = ALFABETO.index(c)
        res += tabela[linha][coluna]
    return res


def decifrar_vigenere(cripto, chave, tabela):
    cripto = normalizar(cripto)
    chave = normalizar(chave)
    if not cripto:
        raise ValueError("Criptograma vazio depois de normalizado")
    if not chave:
        raise ValueError("Chave vazia depois de normalizada")
    res = ""
    for i, c in enumerate(cripto):
        k = chave[i % len(chave)]
        linha = ALFABETO.index(k)
        coluna = tabela[linha].index(c)
        res += ALFABETO[coluna]
    return res
