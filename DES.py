# ---------------------------------------------------------
#  MÓDULO DES – Criptografia DES
# ---------------------------------------------------------

from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def carregar_chave_des(ficheiro):
    """Carrega a chave DES do ficheiro (8 bytes)"""
    with open(ficheiro, "rb") as f:
        chave = f.read()
    
    if len(chave) != 8:
        raise ValueError(f"Chave DES inválida: deve ter exatamente 8 bytes, tem {len(chave)}")
    
    return chave


def cifrar_des(ficheiro_entrada, chave):
    """Cifra um ficheiro usando DES em modo CBC"""
    with open(ficheiro_entrada, "rb") as f:
        dados = f.read()
    
    if not dados:
        raise ValueError("Ficheiro de entrada vazio")
    
    # Gerar IV aleatório (8 bytes para DES)
    iv = get_random_bytes(8)
    
    # Criar cipher em modo CBC
    cipher = DES.new(chave, DES.MODE_CBC, iv)
    
    # Fazer padding e cifrar
    dados_padding = pad(dados, DES.block_size)
    criptograma = cipher.encrypt(dados_padding)
    
    # Retornar IV + criptograma (o IV é necessário para decifrar)
    return iv + criptograma


def decifrar_des(ficheiro_entrada, chave):
    """Decifra um ficheiro usando DES em modo CBC"""
    with open(ficheiro_entrada, "rb") as f:
        dados = f.read()
    
    if len(dados) < 8:
        raise ValueError("Ficheiro cifrado inválido: muito pequeno")
    
    # Extrair IV (primeiros 8 bytes)
    iv = dados[:8]
    criptograma = dados[8:]
    
    # Criar cipher em modo CBC
    cipher = DES.new(chave, DES.MODE_CBC, iv)
    
    # Decifrar e remover padding
    dados_padding = cipher.decrypt(criptograma)
    
    try:
        dados = unpad(dados_padding, DES.block_size)
    except ValueError:
        raise ValueError("Erro ao remover padding - a chave pode estar incorreta")
    
    return dados
