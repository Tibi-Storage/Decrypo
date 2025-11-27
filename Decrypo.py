import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PLAYFAIR import (playfair_cifrar, playfair_decifrar)

from vigenere import (carregar_tabela, carregar_chave, carregar_mensagem,cifrar_vigenere, decifrar_vigenere)




class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Criptografia – Vigenère e Playfair")

        tabs = ttk.Notebook(root)
        tabs.pack(expand=True, fill="both")

        self.tab_vig = ttk.Frame(tabs)
        tabs.add(self.tab_vig, text="Vigenère")

        self.tab_playfair = ttk.Frame(tabs)
        tabs.add(self.tab_playfair, text="Playfair")

        # construir tabs dinamicamente
        self.ctx_vig = self.build_tab(self.tab_vig, "Vigenere")
        self.ctx_play = self.build_tab(self.tab_playfair, "Playfair")

    # -------------------------------------------------------
    # Construção dinâmica de qualquer tab
    # -------------------------------------------------------
    def build_tab(self, frame, algoritmo="Vigenere"):
        ctx = {}  # dicionário que guarda os widgets desta tab

        ttk.Label(frame, text="Ficheiro da tabela:").grid(row=0, column=0, sticky="w")
        ctx["tabela_entry"] = ttk.Entry(frame, width=50)
        ctx["tabela_entry"].grid(row=0, column=1)
        ttk.Button(
            frame, text="Abrir",
            command=lambda: self.escolher_ficheiro(ctx, "tabela")
        ).grid(row=0, column=2)

        ttk.Label(frame, text="Ficheiro da chave:").grid(row=1, column=0, sticky="w")
        ctx["chave_entry"] = ttk.Entry(frame, width=50)
        ctx["chave_entry"].grid(row=1, column=1)
        ttk.Button(
            frame, text="Abrir",
            command=lambda: self.escolher_ficheiro(ctx, "chave")
        ).grid(row=1, column=2)

        ttk.Label(frame, text="Ficheiro da mensagem/criptograma:").grid(row=2, column=0, sticky="w")
        ctx["msg_entry"] = ttk.Entry(frame, width=50)
        ctx["msg_entry"].grid(row=2, column=1)
        ttk.Button(
            frame, text="Abrir",
            command=lambda: self.escolher_ficheiro(ctx, "msg")
        ).grid(row=2, column=2)

        ttk.Button(
            frame, text="Cifrar",
            command=lambda: self.cifrar_generico(ctx, algoritmo)
        ).grid(row=3, column=0, pady=10)

        ttk.Button(
            frame, text="Decifrar",
            command=lambda: self.decifrar_generico(ctx, algoritmo)
        ).grid(row=3, column=1, pady=10)

        ttk.Button(
            frame, text="Guardar Resultado",
            command=lambda: self.guardar_resultado_ctx(ctx)
        ).grid(row=3, column=2, pady=10)

        ctx["resultado_text"] = tk.Text(frame, height=10, width=60)
        ctx["resultado_text"].grid(row=4, column=0, columnspan=3, pady=10)

        return ctx

    # -------------------------------------------------------
    # Escolher ficheiros
    # -------------------------------------------------------
    def escolher_ficheiro(self, ctx, tipo):
        nome = filedialog.askopenfilename()
        if nome:
            entry = ctx[f"{tipo}_entry"]
            entry.delete(0, tk.END)
            entry.insert(0, nome)
            ctx["resultado_text"].delete("1.0", tk.END)

    # -------------------------------------------------------
    # CIFRAR / DECIFRAR genérico
    # -------------------------------------------------------
    def cifrar_generico(self, ctx, algoritmo):
        try:
            chave = carregar_chave(ctx["chave_entry"].get())
            msg = carregar_mensagem(ctx["msg_entry"].get())

            if algoritmo == "Vigenere":
                tabela = carregar_tabela(ctx["tabela_entry"].get())
                resultado = cifrar_vigenere(msg, chave, tabela)

            elif algoritmo == "Playfair":
                resultado = playfair_cifrar(msg, chave)

            else:
                raise ValueError("Algoritmo desconhecido.")

            ctx["resultado_text"].delete("1.0", tk.END)
            ctx["resultado_text"].insert(tk.END, resultado)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def decifrar_generico(self, ctx, algoritmo):
        try:
            if algoritmo == "Vigenere":
                tabela = carregar_tabela(ctx["tabela_entry"].get())
                chave = carregar_chave(ctx["chave_entry"].get())
                cripto = carregar_mensagem(ctx["msg_entry"].get())
                resultado = decifrar_vigenere(cripto, chave, tabela)

            elif algoritmo == "Playfair":
                chave = carregar_chave(ctx["chave_entry"].get())
                cripto = carregar_mensagem(ctx["msg_entry"].get())
                resultado = playfair_decifrar(cripto, chave)

            else:
                raise ValueError("Algoritmo desconhecido.")

            ctx["resultado_text"].delete("1.0", tk.END)
            ctx["resultado_text"].insert(tk.END, resultado)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # -------------------------------------------------------
    # Guardar resultado
    # -------------------------------------------------------
    def guardar_resultado_ctx(self, ctx):
        texto = ctx["resultado_text"].get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Aviso", "Não há resultado para guardar.")
            return

        nome = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Ficheiros de texto", "*.txt")]
        )

        if nome:
            with open(nome, "w", encoding="utf-8") as f:
                f.write(texto)
            messagebox.showinfo("Sucesso", "Resultado guardado com sucesso!")


root = tk.Tk()
App(root)
root.mainloop()
