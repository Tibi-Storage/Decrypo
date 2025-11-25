import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from Decrypo import gerar_tabula_recta, montar_tabela_playfair_de_chave

base = os.path.dirname(__file__)

# write Vigenere table (26 lines)
with open(os.path.join(base, 'tabela_vig.txt'), 'w', encoding='utf-8') as f:
    for line in gerar_tabula_recta():
        f.write(line + '\n')

# write Vigenere key
with open(os.path.join(base, 'chave_vig.txt'), 'w', encoding='utf-8') as f:
    f.write('KEY')

# write message for Vigenere/Playfair
with open(os.path.join(base, 'msg_vig.txt'), 'w', encoding='utf-8') as f:
    f.write('HELLO WORLD')

# generate Playfair table from key 'EXAMPLE' and write as 5 lines
tabela, pos = montar_tabela_playfair_de_chave('EXAMPLE')
with open(os.path.join(base, 'playfair_table.txt'), 'w', encoding='utf-8') as f:
    for row in tabela:
        f.write(''.join(row) + '\n')

# write DES key (hex) and AES key (raw)
with open(os.path.join(base, 'des_key.txt'), 'w', encoding='utf-8') as f:
    f.write('0123456789ABCDEF')  # 8 bytes in hex

with open(os.path.join(base, 'aes_key_128.txt'), 'w', encoding='utf-8') as f:
    f.write('0123456789abcdef')  # 16 bytes raw

# write a small binary file for DES/AES
with open(os.path.join(base, 'data.bin'), 'wb') as f:
    f.write(b'This is test binary data.\x00\x01')

# additional keys/examples for other sizes
# AES-192 (24 bytes) as hex (48 hex chars -> 24 bytes)
with open(os.path.join(base, 'aes_key_192.txt'), 'w', encoding='utf-8') as f:
    f.write('00112233445566778899AABBCCDDEEFF0011223344556677')

# AES-256 (32 bytes) as hex (64 hex chars -> 32 bytes)
with open(os.path.join(base, 'aes_key_256.txt'), 'w', encoding='utf-8') as f:
    f.write('00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF')

# DES raw key file (8 bytes binary)
with open(os.path.join(base, 'des_key_raw.bin'), 'wb') as f:
    f.write(bytes([0x01,0x23,0x45,0x67,0x89,0xAB,0xCD,0xEF]))

print('Exemplos gerados em', base)
