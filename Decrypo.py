import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PLAYFAIR import (playfair_cifrar, playfair_decifrar)
from DES import (carregar_chave_des, cifrar_des, decifrar_des)
from vigenere import (carregar_tabela, carregar_chave, carregar_mensagem,cifrar_vigenere, decifrar_vigenere)




class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Criptografia – Vigenère, Playfair e DES")

        tabs = ttk.Notebook(root)
        tabs.pack(expand=True, fill="both")

        self.tab_vig = ttk.Frame(tabs)
        tabs.add(self.tab_vig, text="Vigenère")

        self.tab_playfair = ttk.Frame(tabs)
        tabs.add(self.tab_playfair, text="Playfair")

        self.tab_des = ttk.Frame(tabs)
        tabs.add(self.tab_des, text="DES")

        # construir tabs dinamicamente
        self.ctx_vig = self.build_tab(self.tab_vig, "Vigenere")
        self.ctx_play = self.build_tab(self.tab_playfair, "Playfair")
        self.ctx_des = self.build_tab_des(self.tab_des)

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
    # Construção da tab DES (específica)
    # -------------------------------------------------------
    def build_tab_des(self, frame):
        ctx = {}

        ttk.Label(frame, text="Ficheiro da chave DES:").grid(row=0, column=0, sticky="w")
        ctx["chave_entry"] = ttk.Entry(frame, width=50)
        ctx["chave_entry"].grid(row=0, column=1)
        ttk.Button(
            frame, text="Abrir",
            command=lambda: self.escolher_ficheiro(ctx, "chave")
        ).grid(row=0, column=2)

        ttk.Label(frame, text="Ficheiro a processar:").grid(row=1, column=0, sticky="w")
        ctx["entrada_entry"] = ttk.Entry(frame, width=50)
        ctx["entrada_entry"].grid(row=1, column=1)
        ttk.Button(
            frame, text="Abrir",
            command=lambda: self.escolher_ficheiro(ctx, "entrada")
        ).grid(row=1, column=2)

        ttk.Button(
            frame, text="Cifrar",
            command=lambda: self.cifrar_des_ctx(ctx)
        ).grid(row=2, column=0, pady=10)

        ttk.Button(
            frame, text="Decifrar",
            command=lambda: self.decifrar_des_ctx(ctx)
        ).grid(row=2, column=1, pady=10)

        ttk.Button(
            frame, text="Guardar Resultado",
            command=lambda: self.guardar_resultado_des(ctx)
        ).grid(row=2, column=2, pady=10)

        ctx["resultado_text"] = tk.Text(frame, height=10, width=60)
        ctx["resultado_text"].grid(row=3, column=0, columnspan=3, pady=10)

        ctx["resultado_binario"] = None

        return ctx

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
    # CIFRAR / DECIFRAR DES
    # -------------------------------------------------------
    def cifrar_des_ctx(self, ctx):
        try:
            chave = carregar_chave_des(ctx["chave_entry"].get())
            ficheiro_entrada = ctx["entrada_entry"].get()

            resultado_binario = cifrar_des(ficheiro_entrada, chave)
            ctx["resultado_binario"] = resultado_binario

            # Mostrar informação sobre o resultado
            ctx["resultado_text"].delete("1.0", tk.END)
            ctx["resultado_text"].insert(tk.END, 
                f"Ficheiro cifrado com sucesso!\n\n"
                f"Tamanho original: {len(resultado_binario) - 8} bytes\n"
                f"Tamanho total (IV + criptograma): {len(resultado_binario)} bytes\n\n"
                f"Clica em 'Guardar Resultado' para salvar o ficheiro cifrado."
            )

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def decifrar_des_ctx(self, ctx):
        try:
            chave = carregar_chave_des(ctx["chave_entry"].get())
            ficheiro_entrada = ctx["entrada_entry"].get()

            resultado_binario = decifrar_des(ficheiro_entrada, chave)
            ctx["resultado_binario"] = resultado_binario

            # Mostrar informação sobre o resultado
            ctx["resultado_text"].delete("1.0", tk.END)
            ctx["resultado_text"].insert(tk.END, 
                f"Ficheiro decifrado com sucesso!\n\n"
                f"Tamanho descompactado: {len(resultado_binario)} bytes\n\n"
                f"Clica em 'Guardar Resultado' para salvar o ficheiro decifrado."
            )

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def guardar_resultado_des(self, ctx):
        if ctx["resultado_binario"] is None:
            messagebox.showwarning("Aviso", "Não há resultado para guardar.")
            return

        nome = filedialog.asksaveasfilename(
            defaultextension="",
            filetypes=[("Todos os ficheiros", "*.*")]
        )

        if nome:
            with open(nome, "wb") as f:
                f.write(ctx["resultado_binario"])
            messagebox.showinfo("Sucesso", "Resultado guardado com sucesso!")

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
