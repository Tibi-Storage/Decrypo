# Decrypo — Aplicação de Cifras Clássicas e Modernas

## Resumo

Aplicação desktop em **Tkinter** para cifrar e decifrar ficheiros usando 4 algoritmos de criptografia:

- **Vigenère** — cifra clássica baseada em deslocamento com chave
- **Playfair** — cifra clássica de pares de caracteres com tabela 5×5
- **DES** (Data Encryption Standard) — cifra simétrica moderna com chave de 8 bytes
- **AES** (Advanced Encryption Standard) — cifra simétrica moderna com chave de 128, 192 ou 256 bits

Todos os algoritmos operam sobre ficheiros em **modo binário** (exceto Vigenère/Playfair que normalizam o texto).

---

## Instalação

### Pré-requisitos

- Python 3.7+
- pip (gestor de pacotes Python)

### Dependências

```bash
pip install pycryptodome
```

Ou criar um ambiente virtual e instalar:

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install pycryptodome
```

---

## Uso

### Executar a aplicação

```bash
python Decrypo.py
```

A GUI abre com 4 abas: **Vigenère**, **Playfair**, **DES** e **AES**.

### Fluxo de utilização

1. **Selecionar ficheiros** — clique em "Abrir" para escolher ficheiros de chave, tabela (se aplicável) e mensagem/entrada.
2. **Validação automática** — a aplicação valida os ficheiros quando os seleciona e mostra o estado na caixa de resultado:
   - ficheiro válido
   - campo inválido
   - Botões desativados = não é possível cifrar/decifrar até corrigir os erros
3. **Cifrar ou Decifrar** — clique no botão correspondente.
4. **Guardar resultado** — clique em "Guardar Resultado" para salvar o ficheiro processado.

---

## Algoritmos

### 1. Vigenère

**Entrada/Saída:**
- Ficheiro de tabela: 26 linhas com 26 caracteres cada (A–Z)
- Ficheiro de chave: texto ASCII (normalizado: maiúsculas, sem caracteres especiais)
- Ficheiro de mensagem: texto ASCII (normalizado)

**Exemplo de uso:**
```
1. Aba "Vigenère"
2. Selecione examples/tabela.txt (tabela 26×26)
3. Selecione examples/chave.txt (chave normalizada)
4. Selecione examples/mensagem.txt (mensagem normalizada)
5. Clique "Cifrar" → resultado é o criptograma normalizado
```

**Validação:**
- Tabela deve ter exatamente 26 linhas com 26 caracteres alfabéticos
- Chave não pode estar vazia após normalização
- Mensagem não pode estar vazia após normalização

---

### 2. Playfair

**Entrada/Saída:**
- Ficheiro de chave: texto ASCII (normalizado)
- Ficheiro de mensagem: texto ASCII (normalizado)
- (Tabela é construída dinamicamente a partir da chave)

**Características:**
- Processa pares de caracteres
- Caracteres 'J' são substituídos por 'I'
- Se a mensagem tem comprimento ímpar, adiciona 'X' no final

**Exemplo de uso:**
```
1. Aba "Playfair"
2. Selecione examples/chave_playfair.txt
3. Selecione examples/mensagem_playfair.txt
4. Clique "Cifrar" → resultado é o criptograma em pares
```

**Validação:**
- Chave não pode estar vazia
- Mensagem não pode estar vazia

---

### 3. DES

**Entrada/Saída:**
- Ficheiro de chave: **exatamente 8 bytes** (binário ou hex/texto)
- Ficheiro de entrada: qualquer ficheiro binário
- Ficheiro de saída: IV (8 bytes) + criptograma

**Modo:** CBC (Cipher Block Chaining) com padding PKCS#7

**Exemplo de uso:**
```
1. Aba "DES"
2. Selecione examples/key_des.bin (ficheiro com 8 bytes)
3. Selecione um ficheiro a cifrar (ex.: documento.pdf)
4. Clique "Cifrar" → gera ficheiro_cifrado.bin (contém IV + criptograma)
5. Para decifrar, selecione o ficheiro cifrado e clique "Decifrar"
```

**Validação:**
- Chave: deve ter exatamente 8 bytes
- Ficheiro de entrada: não pode estar vazio

**Criar uma chave DES:**
```bash
python -c "import os; open('chave_des.bin', 'wb').write(os.urandom(8))"
```

---

### 4. AES

**Entrada/Saída:**
- Ficheiro de chave: 16, 24 ou 32 bytes (binário ou hex/texto)
  - 16 bytes = AES-128
  - 24 bytes = AES-192
  - 32 bytes = AES-256
- Ficheiro de entrada: qualquer ficheiro binário
- Ficheiro de saída: IV (16 bytes) + criptograma

**Modo:** CBC (Cipher Block Chaining) com padding PKCS#7

**Exemplo de uso:**
```
1. Aba "AES"
2. Selecione examples/key_aes128.bin (ficheiro com 16/24/32 bytes)
3. Selecione um ficheiro a cifrar (ex.: arquivo.zip)
4. Clique "Cifrar" → gera arquivo_cifrado.bin (contém IV + criptograma)
5. Para decifrar, selecione o ficheiro cifrado e clique "Decifrar"
```

**Validação:**
- Chave: deve ter 128, 192 ou 256 bits (16, 24 ou 32 bytes)
- Ficheiro de entrada: não pode estar vazio

**Criar uma chave AES:**
```bash
# AES-128 (16 bytes)
python -c "import os; open('chave_aes128.bin', 'wb').write(os.urandom(16))"

# AES-256 (32 bytes)
python -c "import os; open('chave_aes256.bin', 'wb').write(os.urandom(32))"
```

---

## Validação Automática na UI

A aplicação valida os ficheiros **quando são selecionados**:

- **Vigenère/Playfair:** verifica se a tabela, chave e mensagem são válidas (normalizadas, não vazias)
- **DES:** verifica se a chave tem exatamente 8 bytes
- **AES:** verifica se a chave tem 16, 24 ou 32 bytes (exibe em bits: 128/192/256)

---

## Notas Técnicas

### DES/AES com IV

Ambos os algoritmos usam **IV (Initialization Vector)** aleatório:
- O IV é gerado automaticamente durante a cifra
- O IV é preposto ao criptograma no ficheiro de saída
- Na decifra, o IV é extraído do ficheiro (primeiros 8 bytes para DES, 16 para AES)

**Formato do ficheiro cifrado:**
```
[IV (8 ou 16 bytes)] [Criptograma (múltiplo do tamanho de bloco)]
```

### Padding

Ambos usam **PKCS#7**:
- Ficheiros são preenchidos até um múltiplo do tamanho de bloco
- Removido automaticamente na decifra

### Segurança

- **DES:** não recomendado para dados sensíveis (chave pequena)
- **AES:** seguro; use AES-256 para máxima proteção

---


---

## Troubleshooting

| Erro | Causa | Solução |
|------|-------|---------|
| "ModuleNotFoundError: No module named 'Crypto'" | PyCryptodome não instalado | `pip install pycryptodome` |
| "Chave DES inválida: deve ter exatamente 8 bytes" | Ficheiro de chave tem tamanho errado | Criar novo ficheiro com `os.urandom(8)` |
| "Chave AES inválida: deve ter 16, 24 ou 32 bytes" | Ficheiro de chave tem tamanho errado | Criar novo com 16, 24 ou 32 bytes |
| "Erro ao remover padding — a chave pode estar incorreta" | Chave ou ficheiro cifrado inválido | Verificar se a chave é a mesma usada na cifra |
| Botões desativados | Validação falha | Verificar mensagens na caixa de resultado |

---

