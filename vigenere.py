import string

ALFABETO = string.ascii_uppercase

def normalizar(txt):
    txt = txt.upper()
    return "".join(c for c in txt if c in ALFABETO)

def carregar_tabela(ficheiro):
    tabela = []
    with open(ficheiro, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip().upper()
            if len(linha) == 26 and all(c in ALFABETO for c in linha):
                tabela.append(linha)
    if len(tabela) != 26:
        raise ValueError("Tabela inválida: Deve conter 26 linhas válidas")
    return tabela

def carregar_chave(ficheiro):
    with open(ficheiro, "r", encoding="utf-8") as f:
        chave = f.read()
    return normalizar(chave)

def carregar_mensagem(ficheiro):
    with open(ficheiro, "r", encoding="utf-8") as f:
        msg = f.read()
    return normalizar(msg)

def cifrar_vigenere(msg, chave, tabela):
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
