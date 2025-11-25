def ler_chave_texto(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def parse_key_bytes(text):
    txt = text.strip()
    hexchars = set('0123456789abcdefABCDEF')
    if all(c in hexchars for c in txt) and len(txt) % 2 == 0:
        try:
            return bytes.fromhex(txt)
        except Exception:
            pass
    return txt.encode('utf-8')


def is_visible_ascii_bytes(b):
    return all(32 <= c <= 126 for c in b)
