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

def main():
    tabela = gerar_tabula_recta()
    op = input("Pretende cifrar (C) ou decifrar (D)? ").strip().upper()
    if op == "C":
        msg = input("Qual a mensagem a cifrar: ")
        chave = input("Chave: ")
        cripto = cifrar_vigenere(msg, chave, tabela)
        print("Criptograma: ", cripto)
    elif op == "D":
        cripto = input("Qual é o criptograma: ")
        chave = input("Chave: ")
        msg = decifrar_vigenere(cripto, chave, tabela)
        print("Mensagem decifrada: ", msg)
    else:
        print("Opção inválida.")

if __name__== "__main__":
    main()