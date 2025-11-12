def montar_tabela(chave):
    chave = chave.upper()
    chave = chave.replace("J", "I")
    filtrada = ""
    for c in chave:
        if 'A' <= c <= 'Z' and c != 'J':
            if c not in filtrada:
                filtrada +=c
    alfabeto = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for c in alfabeto:
        if c not in filtrada:
            filtrada += c
    tabela = [list(filtrada[i:i+5]) for i in range (0, 25, 5)]
    pos = {}
    for i in range(5):
        for j in range(5):
            pos[tabela[i][j]] = (i, j)
    return tabela, pos

def preparar_texto(txt):
    txt = txt.upper()
    txt = txt.replace("J", "I")
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
        if modo == "cifrar":
            ja2, jb2 = (ja + 1) % 5, (jb + 1) % 5
        else:
            ja2, jb2 = (ja - 1) % 5, (jb - 1) % 5
        return tabela[ia][ja2] + tabela[ib][jb2]
    if ja == jb:
        if modo == "cifrar":
            ia2, ib2 = (ia + 1) % 5, (ib + 1) % 5
        else:
            ia2, ib2 = (ia - 1) % 5, (ib - 1) % 5
        return tabela[ia2][ja] + tabela[ib2][jb]
    return tabela[ia][jb] + tabela[ib][ja]

def playfair_cifrar(msg, chave):
    tabela, pos = montar_tabela(chave)
    pares = preparar_texto(msg)
    res = ""
    for p in pares:
        res += transformar_par(p, pos, tabela, "cifrar")
    return res

def playfair_decifrar(msg, chave):
    tabela, pos = montar_tabela(chave)
    msg = msg.upper().replace("J", "I")
    msg = ''.join(c for c in msg if 'A' <= c <= 'Z')
    pares = [msg[i:i+2] for i in range(0, len(msg), 2)]
    res = ""
    for p in pares:
        res += transformar_par(p, pos, tabela, "decifrar")
    return res



print("Digite 1 para CIFRAR ou 2 para DECIFRAR: ")
op = input("Opção: ")

if op == "1":
    msg = input("Digite a mensagem a cifrar: ")
    chave = input("Digite a chave: ")
    print("Criptograma: ", playfair_cifrar(msg, chave))

elif op == "2":
    msg = input("Digite a criptograma a decifrar: ")
    chave = input("Digite a chave: ")
    print("Mensagem: ", playfair_decifrar(msg, chave))

else:
    print("Opção inválida!")






    
