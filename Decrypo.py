import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog

# ensure local modules are importable when running tests or as script
sys.path.insert(0, os.path.dirname(__file__))

# Re-export functions from modules to keep backwards compatibility
try:
    from vigenere import *
except Exception:
    try:
        from VIGENERE import *
    except Exception:
        pass

try:
    from playfair import *
except Exception:
    try:
        from PLAYFAIR import *
    except Exception:
        pass

try:
    from modern import *
except Exception:
    try:
        from MODERN import *
    except Exception:
        pass

try:
    from utils import *
except Exception:
    try:
        from UTILS import *
    except Exception:
        pass


class App:
    def __init__(self, root):
        self.root = root
        root.title('Decrypo - Cifras Clássicas e Modernas')

        self.cipher_var = tk.StringVar(value='VIGENERE')
        self.op_var = tk.StringVar(value='CIFRAR')
        self.table_path = tk.StringVar()
        self.key_path = tk.StringVar()
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()

        row = 0
        tk.Label(root, text='Cifra:').grid(row=row, column=0, sticky='w')
        tk.OptionMenu(root, self.cipher_var, 'VIGENERE', 'PLAYFAIR', 'DES', 'AES', command=self._on_cipher_change).grid(row=row, column=1, sticky='we')
        row += 1
        tk.Label(root, text='Operação:').grid(row=row, column=0, sticky='w')
        tk.OptionMenu(root, self.op_var, 'CIFRAR', 'DECIFRAR').grid(row=row, column=1, sticky='we')
        row += 1

        self.table_label = tk.Label(root, text='Ficheiro tabela (Vigenère / Playfair):')
        self.table_label.grid(row=row, column=0, sticky='w')
        self.table_entry = tk.Entry(root, textvariable=self.table_path, width=50)
        self.table_entry.grid(row=row, column=1, sticky='we')
        self.table_button = tk.Button(root, text='Selecionar', command=self.select_table)
        self.table_button.grid(row=row, column=2)
        row += 1

        self.key_label = tk.Label(root, text='Ficheiro chave (DES/AES ou Vigenère):')
        self.key_label.grid(row=row, column=0, sticky='w')
        self.key_entry = tk.Entry(root, textvariable=self.key_path, width=50)
        self.key_entry.grid(row=row, column=1, sticky='we')
        self.key_button = tk.Button(root, text='Selecionar', command=self.select_key)
        self.key_button.grid(row=row, column=2)
        row += 1

        tk.Label(root, text='Ficheiro entrada:').grid(row=row, column=0, sticky='w')
        self.input_entry = tk.Entry(root, textvariable=self.input_path, width=50)
        self.input_entry.grid(row=row, column=1, sticky='we')
        self.input_button = tk.Button(root, text='Selecionar', command=self.select_input)
        self.input_button.grid(row=row, column=2)
        row += 1

        tk.Label(root, text='Ficheiro saída:').grid(row=row, column=0, sticky='w')
        self.output_entry = tk.Entry(root, textvariable=self.output_path, width=50)
        self.output_entry.grid(row=row, column=1, sticky='we')
        self.output_button = tk.Button(root, text='Selecionar', command=self.select_output)
        self.output_button.grid(row=row, column=2)
        row += 1

        tk.Button(root, text='Executar', command=self.execute).grid(row=row, column=0, columnspan=3, sticky='we')

        self._on_cipher_change(self.cipher_var.get())

    def _on_cipher_change(self, _):
        c = self.cipher_var.get()
        # Update labels to be explicit depending on selected cipher
        if c == 'VIGENERE':
            self.table_label.config(text='Ficheiro tabela (Vigenère - 26x26):')
            self.key_label.config(text='Ficheiro chave (Vigenère):')
            # enable both table and key selection
            self.table_entry.config(state='normal')
            self.table_button.config(state='normal')
            self.key_entry.config(state='normal')
            self.key_button.config(state='normal')
        elif c == 'PLAYFAIR':
            self.table_label.config(text='Ficheiro tabela Playfair (5x5 - 25 letras):')
            self.key_label.config(text='Ficheiro chave (não aplicável para Playfair)')
            # table required, key not applicable
            self.table_entry.config(state='normal')
            self.table_button.config(state='normal')
            self.key_entry.delete(0, 'end')
            self.key_entry.config(state='disabled')
            self.key_button.config(state='disabled')
        elif c == 'DES':
            self.table_label.config(text='Ficheiro tabela (não aplicável para DES)')
            self.key_label.config(text='Ficheiro chave (DES - 8 bytes ou 16 hex dígitos)')
            # key required, table not applicable
            self.table_entry.delete(0, 'end')
            self.table_entry.config(state='disabled')
            self.table_button.config(state='disabled')
            self.key_entry.config(state='normal')
            self.key_button.config(state='normal')
        elif c == 'AES':
            self.table_label.config(text='Ficheiro tabela (não aplicável para AES)')
            self.key_label.config(text='Ficheiro chave (AES - 16/24/32 bytes ou hex)')
            # key required, table not applicable
            self.table_entry.delete(0, 'end')
            self.table_entry.config(state='disabled')
            self.table_button.config(state='disabled')
            self.key_entry.config(state='normal')
            self.key_button.config(state='normal')

    def select_table(self):
        p = filedialog.askopenfilename(title='Selecionar ficheiro de tabela (Vigenere/Playfair)')
        if p:
            self.table_path.set(p)

    def select_key(self):
        p = filedialog.askopenfilename(title='Selecionar ficheiro de chave (DES/AES)')
        if p:
            self.key_path.set(p)

    def select_input(self):
        p = filedialog.askopenfilename(title='Selecionar ficheiro de entrada')
        if p:
            self.input_path.set(p)

    def select_output(self):
        p = filedialog.asksaveasfilename(title='Selecionar ficheiro de saída', defaultextension='.txt')
        if p:
            self.output_path.set(p)

    def execute(self):
        cipher = self.cipher_var.get()
        op = self.op_var.get()
        inpath = self.input_path.get()
        outpath = self.output_path.get()
        if not inpath or not outpath:
            messagebox.showerror('Erro', 'Escolha ficheiro de entrada e saída')
            return
        try:
            if cipher == 'VIGENERE':
                # Vigenere: tabela e chave devem ser lidas de ficheiros de texto
                if not self.table_path.get():
                    messagebox.showerror('Erro', 'Escolha ficheiro de tabela para Vigenère')
                    return
                if not self.key_path.get():
                    messagebox.showerror('Erro', 'Escolha ficheiro de chave para Vigenère')
                    return
                # validate table and key files contain only visible ASCII
                tbl_bytes = open(self.table_path.get(), 'rb').read()
                if not is_visible_ascii_bytes(tbl_bytes):
                    raise ValueError('Ficheiro de tabela tem de conter apenas caracteres ASCII visíveis')
                key_bytes = open(self.key_path.get(), 'rb').read()
                if not is_visible_ascii_bytes(key_bytes):
                    raise ValueError('Ficheiro de chave tem de conter apenas caracteres ASCII visíveis')
                tabela = ler_tabela_vigenere(self.table_path.get())
                chave = ler_chave_texto(self.key_path.get())
                txt = open(inpath, 'r', encoding='utf-8').read()
                if not is_visible_ascii_bytes(txt.encode('utf-8')):
                    raise ValueError('Ficheiro de entrada tem de conter apenas caracteres ASCII visíveis')
                if op == 'CIFRAR':
                    res = cifrar_vigenere(txt, chave, tabela)
                else:
                    res = decifrar_vigenere(txt, chave, tabela)
                with open(outpath, 'w', encoding='utf-8') as f:
                    f.write(res)
                messagebox.showinfo('OK', 'Operação concluída')

            elif cipher == 'PLAYFAIR':
                # Playfair: deve ler a tabela completa (chave + restantes) de ficheiro de texto
                if not self.table_path.get():
                    messagebox.showerror('Erro', 'Escolha ficheiro de tabela Playfair')
                    return
                # validate table file and input file contain only visible ASCII
                tbl_bytes = open(self.table_path.get(), 'rb').read()
                if not is_visible_ascii_bytes(tbl_bytes):
                    raise ValueError('Ficheiro de tabela Playfair tem de conter apenas caracteres ASCII visíveis')
                tabela, pos = ler_tabela_playfair(self.table_path.get())
                in_bytes = open(inpath, 'rb').read()
                if not is_visible_ascii_bytes(in_bytes):
                    raise ValueError('Ficheiro de entrada tem de conter apenas caracteres ASCII visíveis')
                txt = in_bytes.decode('ascii')
                if op == 'CIFRAR':
                    res = playfair_cifrar(txt, tabela, pos)
                else:
                    res = playfair_decifrar(txt, tabela, pos)
                with open(outpath, 'w', encoding='utf-8') as f:
                    f.write(res)
                messagebox.showinfo('OK', 'Operação concluída')

            elif cipher == 'DES':
                if not self.key_path.get():
                    messagebox.showerror('Erro', 'Escolha ficheiro de chave para DES')
                    return
                key_txt = ler_chave_texto(self.key_path.get())
                key_bytes = parse_key_bytes(key_txt)
                data = open(inpath, 'rb').read()
                if op == 'CIFRAR':
                    out = des_encrypt(key_bytes, data)
                else:
                    out = des_decrypt(key_bytes, data)
                with open(outpath, 'wb') as f:
                    f.write(out)
                messagebox.showinfo('OK', 'Operação concluída')

            elif cipher == 'AES':
                if not self.key_path.get():
                    messagebox.showerror('Erro', 'Escolha ficheiro de chave para AES')
                    return
                key_txt = ler_chave_texto(self.key_path.get())
                key_bytes = parse_key_bytes(key_txt)
                data = open(inpath, 'rb').read()
                if op == 'CIFRAR':
                    out = aes_encrypt(key_bytes, data)
                else:
                    out = aes_decrypt(key_bytes, data)
                with open(outpath, 'wb') as f:
                    f.write(out)
                messagebox.showinfo('OK', 'Operação concluída')
            else:
                messagebox.showerror('Erro', 'Cifra desconhecida')
        except Exception as e:
            messagebox.showerror('Erro', str(e))


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
