import os
import sys
# Garantir que o raiz do projecto está no sys.path para importar módulos locais
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from AES import carregar_chave_aes, cifrar_aes, decifrar_aes

KEY_FILE = 'examples/key_aes128.bin'
PLAINTEXT_FILE = 'examples/plain_test.bin'
CIPHER_FILE = 'examples/plain_test.aes'

# Criar chave AES (16 bytes)
with open(KEY_FILE, 'wb') as f:
    f.write(os.urandom(16))

# Criar ficheiro de teste
original = b"Este e um texto de teste para AES. Contem bytes e texto utf-8." 
with open(PLAINTEXT_FILE, 'wb') as f:
    f.write(original)

# Carregar chave (pode ser binário ou texto/hex no ficheiro)
chave = carregar_chave_aes(KEY_FILE)

# Cifrar -> obter bytes (IV + criptograma) e gravar
cript = cifrar_aes(PLAINTEXT_FILE, chave)
with open(CIPHER_FILE, 'wb') as f:
    f.write(cript)

# Decifrar a partir do ficheiro cifrado
recuperado = decifrar_aes(CIPHER_FILE, chave)

# Verificar integridade
if recuperado == original:
    print('OK: AES roundtrip successful')
    # Print sizes for info
    print('plaintext bytes:', len(original))
    print('cipher bytes:', len(cript))
    exit(0)
else:
    print('ERRO: roundtrip mismatch')
    print('original:', original)
    print('recovered:', recuperado)
    exit(2)
