import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from playfair import (
    ler_tabela_playfair,
    montar_tabela_playfair_de_chave,
    preparar_texto_playfair,
    playfair_cifrar,
    playfair_decifrar,
)
from utils import is_visible_ascii_bytes


class TestPlayfair(unittest.TestCase):
    def setUp(self):
        self.base = os.path.join(os.path.dirname(__file__), '..', 'examples')
        self.base = os.path.normpath(self.base)

    def test_read_table_and_roundtrip(self):
        table_path = os.path.join(self.base, 'playfair_table.txt')
        msg_path = os.path.join(self.base, 'msg_vig.txt')

        tabela, pos = ler_tabela_playfair(table_path)
        self.assertIsNotNone(tabela)

        txt = open(msg_path, 'r', encoding='utf-8').read()
        # files should contain only visible ASCII
        self.assertTrue(is_visible_ascii_bytes(txt.encode('utf-8')))

        prepared = ''.join(preparar_texto_playfair(txt))
        cipher = playfair_cifrar(txt, tabela, pos)
        dec = playfair_decifrar(cipher, tabela, pos)

        self.assertEqual(dec, prepared)


if __name__ == '__main__':
    unittest.main()
