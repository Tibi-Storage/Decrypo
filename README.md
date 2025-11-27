Decrypo - Aplicação de Cifras Clássicas e Modernas

Resumo
- GUI em Tkinter para cifrar/decifrar ficheiros usando Vigenère, Playfair, DES e AES.
- Vigenère e Playfair implementadas de raiz (regras do enunciado).
- DES e AES implementadas usando bibliotecas criptográficas (PyCryptodome preferencialmente).
- 
- Execute a aplicação:

```powershell
python Decrypo.py
```

Formato dos ficheiros
- Vigenère:
  - Ficheiro de tabela: 26 linhas com 26 letras cada (A-Z), ou bloco contínuo de 26*26 letras.
  - Ficheiro de chave: texto ASCII (a aplicação aceita texto raw ou hex). A mensagem/criptograma deve conter apenas caracteres ASCII visíveis.
- Playfair:
  - Ficheiro de tabela: 25 caracteres (A-Z, sem J, ou J tratado como I), ordenados conforme a tabela 5x5.
  - A mensagem/criptograma deve conter apenas caracteres ASCII visíveis.
- DES/AES:
  - Ficheiro de chave: texto raw (ASCII) ou chave em hex. DES: 8 bytes; AES: 16/24/32 bytes.
  - Os ficheiros de entrada são processados em modo binário. O ficheiro de saída binário contém IV || ciphertext.

Notas técnicas
- DES/AES usam CBC com padding PKCS7. A saída gravada em ficheiros binários contém o IV no início seguido do ciphertext.
- Para DECIFRAR ficheiros DES/AES, a aplicação espera que o IV esteja no início do ficheiro.

Testes
- Existem testes unitários em `tests/test_decrypo.py`.
- Executar:

```powershell
python -m unittest discover -v
```
