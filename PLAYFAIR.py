"""Playfair CLI wrapper compatible with the GUI in `Decrypo.py`.

This module re-uses the implementations in `PLAYFAIR.py` (present in the
repository) and provides a small command-line `main()` that:
- asks the user to choose CIFRAR or DECIFRAR
- asks for the Playfair table file (text containing 25 letters)
- asks for the input message/criptograma file
- validates that files contain only visible ASCII characters
- prints the result (and returns it)

The GUI (`Decrypo.py`) imports `ler_tabela_playfair`, `playfair_cifrar`
and `playfair_decifrar` from this module, so keep the names available.
"""

from PLAYFAIR import ler_tabela_playfair, playfair_cifrar, playfair_decifrar
from utils import is_visible_ascii_bytes


def main():
    print("Digite 1 para CIFRAR ou 2 para DECIFRAR:")
    op = input("Opção: ").strip()

    table_path = input("Ficheiro com a tabela Playfair (5x5 - 25 letras): ").strip()
    if not table_path:
        print("É necessário indicar o ficheiro com a tabela Playfair.")
        return

    try:
        tabela, pos = ler_tabela_playfair(table_path)
    except Exception as e:
        print("Erro ao ler a tabela Playfair:", e)
        return

    inpath = input("Ficheiro com a mensagem/criptograma: ").strip()
    if not inpath:
        print("É necessário indicar o ficheiro de entrada.")
        return

    try:
        b = open(inpath, 'rb').read()
    except Exception as e:
        print("Erro ao ler ficheiro de entrada:", e)
        return

    if not is_visible_ascii_bytes(b):
        print("Erro: ficheiro tem de conter apenas caracteres ASCII visíveis (32-126).")
        return

    # safe to decode as ASCII because we validated the bytes
    txt = b.decode('ascii')

    try:
        if op == '1':
            res = playfair_cifrar(txt, tabela, pos)
            print('Criptograma: ', res)
        elif op == '2':
            res = playfair_decifrar(txt, tabela, pos)
            print('Mensagem: ', res)
        else:
            print('Opção inválida!')
    except Exception as e:
        print('Erro durante operação Playfair:', e)


if __name__ == '__main__':
    main()
"""Playfair cipher helper functions."""

def montar_tabela_playfair_de_chave(chave):
    chave = chave.upper()
    chave = chave.replace('J', 'I')
    filtrada = ''
    for c in chave:
        if 'A' <= c <= 'Z' and c != 'J':
            if c not in filtrada:
                filtrada += c
    alfabeto = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    for c in alfabeto:
        if c not in filtrada:
            filtrada += c
    tabela = [list(filtrada[i:i+5]) for i in range(0, 25, 5)]
    pos = {}
    for i in range(5):
        for j in range(5):
            pos[tabela[i][j]] = (i, j)
    return tabela, pos


def ler_tabela_playfair(path):
    if not path:
        return None
    with open(path, 'r', encoding='utf-8') as f:
        texto = ''.join(line.strip().upper() for line in f if line.strip())
    texto = texto.replace('J', 'I')
    conteudo = ''.join(c for c in texto if 'A' <= c <= 'Z')
    if len(conteudo) < 25:
        raise ValueError('Ficheiro de tabela Playfair inválido: precisa de 25 letras')
    conteudo = conteudo[:25]
    tabela = [list(conteudo[i:i+5]) for i in range(0, 25, 5)]
    pos = {}
    for i in range(5):
        for j in range(5):
            pos[tabela[i][j]] = (i, j)
    return tabela, pos


def preparar_texto_playfair(txt):
    txt = txt.upper()
    txt = txt.replace('J', 'I')
    txt = ''.join(c for c in txt if 'A' <= c <= 'Z')
    pares = []
    i = 0
    while i < len(txt):
        a = txt[i]
        if i + 1 < len(txt):
            b = txt[i+1]
            if a == b:
                pares.append(a + 'X')
                i += 1
            else:
                pares.append(a + b)
                i += 2
        else:
            pares.append(a + 'X')
            i += 1
    return pares


def transformar_par(par, pos, tabela, modo):
    a, b = par[0], par[1]
    ia, ja = pos[a]
    ib, jb = pos[b]
    if ia == ib:
        if modo == 'cifrar':
            ja2, jb2 = (ja + 1) % 5, (jb + 1) % 5
        else:
            ja2, jb2 = (ja - 1) % 5, (jb - 1) % 5
        return tabela[ia][ja2] + tabela[ib][jb2]
    if ja == jb:
        if modo == 'cifrar':
            ia2, ib2 = (ia + 1) % 5, (ib + 1) % 5
        else:
            ia2, ib2 = (ia - 1) % 5, (ib - 1) % 5
        return tabela[ia2][ja] + tabela[ib2][jb]
    return tabela[ia][jb] + tabela[ib][ja]


def playfair_cifrar(msg, tabela, pos):
    pares = preparar_texto_playfair(msg)
    res = ''
    for p in pares:
        res += transformar_par(p, pos, tabela, 'cifrar')
    return res


def playfair_decifrar(msg, tabela, pos):
    msg = msg.upper().replace('J', 'I')
    msg = ''.join(c for c in msg if 'A' <= c <= 'Z')
    pares = [msg[i:i+2] for i in range(0, len(msg), 2)]
    res = ''
    for p in pares:
        res += transformar_par(p, pos, tabela, 'decifrar')
    return res







