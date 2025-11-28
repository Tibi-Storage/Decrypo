# ---------------------------------------------------------
#  MÓDULO AES – Criptografia AES (CBC) - suporta 128/192/256 bits
# ---------------------------------------------------------

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def carregar_chave_aes(ficheiro):
    """Lê a chave AES de um ficheiro binário ou de texto. Retorna bytes com comprimento 16/24/32."""
    # Tentar ler em binário primeiro
    try:
        with open(ficheiro, 'rb') as f:
            dados = f.read()
    except Exception as e:
        raise

    # Se o ficheiro contiver texto com nova linha, remover espaços
    if len(dados) == 0:
        raise ValueError('Ficheiro de chave vazio')

    # Se aparentar ser texto com hex ou com chars imprimíveis, permitir ambos:
    # - Se contém apenas hex e tamanho par: converter de hex
    # - Caso contrário, usar bytes diretos (trim/extend não é permitido)
    # Tentar decodificar como ASCII e interpretar hex
    try:
        s = dados.decode('ascii').strip()
        # aceitar hex sem 0x
        if all(c in '0123456789abcdefABCDEF' for c in s) and len(s) % 2 == 0:
            chave = bytes.fromhex(s)
        else:
            # usar a representação ascii direta (por exemplo chave textual)
            chave = s.encode('utf-8')
    except Exception:
        chave = dados

    if len(chave) not in (16, 24, 32):
        raise ValueError(f'Chave AES inválida: deve ter 16, 24 ou 32 bytes (tem {len(chave)})')

    return chave


def cifrar_aes(ficheiro_entrada, chave):
    """Cifra ficheiro em modo CBC. Retorna IV (16 bytes) + criptograma."""
    with open(ficheiro_entrada, 'rb') as f:
        dados = f.read()

    if dados is None:
        raise ValueError('Ficheiro de entrada não pôde ser lido')

    iv = get_random_bytes(16)
    cipher = AES.new(chave, AES.MODE_CBC, iv)
    dados_pad = pad(dados, AES.block_size)
    criptograma = cipher.encrypt(dados_pad)
    return iv + criptograma


def decifrar_aes(ficheiro_entrada, chave):
    """Decifra ficheiro em modo CBC. Retorna bytes do ficheiro original."""
    with open(ficheiro_entrada, 'rb') as f:
        dados = f.read()

    if len(dados) < 16:
        raise ValueError('Ficheiro cifrado inválido: muito pequeno')

    iv = dados[:16]
    criptograma = dados[16:]
    cipher = AES.new(chave, AES.MODE_CBC, iv)
    dados_pad = cipher.decrypt(criptograma)
    try:
        dados = unpad(dados_pad, AES.block_size)
    except ValueError:
        raise ValueError('Erro ao remover padding - a chave pode estar incorreta')
    return dados
