import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PLAYFAIR import (playfair_cifrar, playfair_decifrar)
from DES import (carregar_chave_des, cifrar_des, decifrar_des)
from AES import (carregar_chave_aes, cifrar_aes, decifrar_aes)
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
        
        self.tab_aes = ttk.Frame(tabs)
        tabs.add(self.tab_aes, text="AES")

        # construir tabs dinamicamente
        self.ctx_vig = self.build_tab(self.tab_vig, "Vigenere")
        self.ctx_play = self.build_tab(self.tab_playfair, "Playfair")
        self.ctx_des = self.build_tab_des(self.tab_des)
        self.ctx_aes = self.build_tab_aes(self.tab_aes)

    # -------------------------------------------------------
    # Construção dinâmica de qualquer tab
    # -------------------------------------------------------
    def build_tab(self, frame, algoritmo="Vigenere"):
        ctx = {}  # dicionário que guarda os widgets desta tab
        ctx["algoritmo"] = algoritmo

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

        btn = ttk.Button(frame, text="Cifrar", command=lambda: self.cifrar_generico(ctx, algoritmo))
        btn.grid(row=3, column=0, pady=10)
        ctx["cifrar_btn"] = btn

        btn2 = ttk.Button(frame, text="Decifrar", command=lambda: self.decifrar_generico(ctx, algoritmo))
        btn2.grid(row=3, column=1, pady=10)
        ctx["decifrar_btn"] = btn2

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
        ctx["algoritmo"] = "DES"

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

        btn = ttk.Button(frame, text="Cifrar", command=lambda: self.cifrar_des_ctx(ctx))
        btn.grid(row=2, column=0, pady=10)
        ctx["cifrar_btn"] = btn

        btn2 = ttk.Button(frame, text="Decifrar", command=lambda: self.decifrar_des_ctx(ctx))
        btn2.grid(row=2, column=1, pady=10)
        ctx["decifrar_btn"] = btn2

        ttk.Button(
            frame, text="Guardar Resultado",
            command=lambda: self.guardar_resultado_des(ctx)
        ).grid(row=2, column=2, pady=10)

        ctx["resultado_text"] = tk.Text(frame, height=10, width=60)
        ctx["resultado_text"].grid(row=3, column=0, columnspan=3, pady=10)

        ctx["resultado_binario"] = None

        return ctx

    # -------------------------------------------------------
    # Construção da tab AES (específica)
    # -------------------------------------------------------
    def build_tab_aes(self, frame):
        ctx = {}
        ctx["algoritmo"] = "AES"

        ttk.Label(frame, text="Ficheiro da chave AES:").grid(row=0, column=0, sticky="w")
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

        btn = ttk.Button(frame, text="Cifrar", command=lambda: self.cifrar_aes_ctx(ctx))
        btn.grid(row=2, column=0, pady=10)
        ctx["cifrar_btn"] = btn

        btn2 = ttk.Button(frame, text="Decifrar", command=lambda: self.decifrar_aes_ctx(ctx))
        btn2.grid(row=2, column=1, pady=10)
        ctx["decifrar_btn"] = btn2

        ttk.Button(
            frame, text="Guardar Resultado",
            command=lambda: self.guardar_resultado_aes(ctx)
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
            # validar automaticamente o contexto quando o utilizador escolhe um ficheiro
            try:
                ok, mensagens = self.validar_ctx(ctx, tipo)
                self.update_ui_validation(ctx, ok, mensagens)
            except Exception as e:
                # mostrar erro de validação
                ctx["resultado_text"].insert(tk.END, f"Erro de validação: {e}")

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
    # Validação dos ficheiros / chaves mostrada no UI
    # -------------------------------------------------------
    def validar_ctx(self, ctx, tipo=None):
        """Valida os ficheiros indicados no ctx dependendo do algoritmo e escreve mensagens em resultado_text."""
        alg = ctx.get("algoritmo", "Vigenere")
        out = []

        import os

        def file_exists(path):
            return bool(path) and os.path.isfile(path) and os.path.getsize(path) > 0

        if alg == "Vigenere":
            # tabela
            tabela_path = ctx.get("tabela_entry", None) and ctx["tabela_entry"].get()
            if tabela_path:
                try:
                    tabela = carregar_tabela(tabela_path)
                    out.append(f"Tabela Vigenère válida: {len(tabela)} linhas")
                except Exception as e:
                    out.append(f"Tabela inválida: {e}")

            chave_path = ctx.get("chave_entry", None) and ctx["chave_entry"].get()
            if chave_path:
                try:
                    chave = carregar_chave(chave_path)
                    if not chave:
                        raise ValueError("Chave vazia depois da normalização")
                    out.append(f"Chave Vigenère válida: {len(chave)} caracteres (normalizada)")
                except Exception as e:
                    out.append(f"Chave inválida: {e}")

            msg_path = ctx.get("msg_entry", None) and ctx["msg_entry"].get()
            if msg_path:
                try:
                    msg = carregar_mensagem(msg_path)
                    if not msg:
                        raise ValueError("Mensagem vazia depois da normalização")
                    out.append(f"Mensagem válida: {len(msg)} caracteres (normalizada)")
                except Exception as e:
                    out.append(f"Mensagem inválida: {e}")

        elif alg == "Playfair":
            chave_path = ctx.get("chave_entry", None) and ctx["chave_entry"].get()
            if chave_path:
                try:
                    # Reuse carregar_chave to normalizar
                    chave = carregar_chave(chave_path)
                    if not chave:
                        raise ValueError("Chave Playfair vazia depois da normalização")
                    out.append(f"Chave Playfair válida: {len(chave)} caracteres (normalizada)")
                except Exception as e:
                    out.append(f"Chave inválida: {e}")

            msg_path = ctx.get("msg_entry", None) and ctx["msg_entry"].get()
            if msg_path:
                try:
                    msg = carregar_mensagem(msg_path)
                    if not msg:
                        raise ValueError("Mensagem vazia depois da normalização")
                    out.append(f"Mensagem Playfair válida: {len(msg)} caracteres (normalizada)")
                except Exception as e:
                    out.append(f"Mensagem inválida: {e}")

        elif alg == "DES":
            chave_path = ctx.get("chave_entry", None) and ctx["chave_entry"].get()
            if chave_path:
                try:
                    k = carregar_chave_des(chave_path)
                    out.append(f"Chave DES válida: {len(k)} bytes")
                except Exception as e:
                    out.append(f"Chave DES inválida: {e}")

            entrada = ctx.get("entrada_entry", None) and ctx["entrada_entry"].get()
            if entrada:
                if file_exists(entrada):
                    size = os.path.getsize(entrada)
                    out.append(f"Ficheiro de entrada DES válido: {size} bytes")
                else:
                    out.append("Ficheiro de entrada DES inválido ou vazio")

        elif alg == "AES":
            chave_path = ctx.get("chave_entry", None) and ctx["chave_entry"].get()
            if chave_path:
                try:
                    k = carregar_chave_aes(chave_path)
                    out.append(f"Chave AES válida: {len(k)*8} bits ({len(k)} bytes)")
                except Exception as e:
                    out.append(f"Chave AES inválida: {e}")

            entrada = ctx.get("entrada_entry", None) and ctx["entrada_entry"].get()
            if entrada:
                if file_exists(entrada):
                    size = os.path.getsize(entrada)
                    out.append(f"Ficheiro de entrada AES válido: {size} bytes")
                else:
                    out.append("Ficheiro de entrada AES inválido ou vazio")

        else:
            out.append("Algoritmo desconhecido para validação")

        # Mostrar o resultado da validação no widget
        ctx["resultado_text"].delete("1.0", tk.END)
        if out:
            for linha in out:
                ctx["resultado_text"].insert(tk.END, linha + "\n")
        else:
            ctx["resultado_text"].insert(tk.END, "Nenhum ficheiro selecionado ainda para validação.")

        # Retornar True se todas validações principais estiverem OK (heurística)
        # Considera OK se não há linhas com 'inválid' ou 'Erro'
        ok = all(("inválid" not in l.lower() and "erro" not in l.lower() and "nenhum" not in l.lower()) for l in out)
        return ok, out

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

    # -------------------------------------------------------
    # CIFRAR / DECIFRAR AES
    # -------------------------------------------------------
    def cifrar_aes_ctx(self, ctx):
        try:
            chave = carregar_chave_aes(ctx["chave_entry"].get())
            ficheiro_entrada = ctx["entrada_entry"].get()

            resultado_binario = cifrar_aes(ficheiro_entrada, chave)
            ctx["resultado_binario"] = resultado_binario

            ctx["resultado_text"].delete("1.0", tk.END)
            ctx["resultado_text"].insert(tk.END, 
                f"Ficheiro cifrado com sucesso!\n\n"
                f"Tamanho total (IV + criptograma): {len(resultado_binario)} bytes\n\n"
                f"Clica em 'Guardar Resultado' para salvar o ficheiro cifrado."
            )

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def decifrar_aes_ctx(self, ctx):
        try:
            chave = carregar_chave_aes(ctx["chave_entry"].get())
            ficheiro_entrada = ctx["entrada_entry"].get()

            resultado_binario = decifrar_aes(ficheiro_entrada, chave)
            ctx["resultado_binario"] = resultado_binario

            ctx["resultado_text"].delete("1.0", tk.END)
            ctx["resultado_text"].insert(tk.END, 
                f"Ficheiro decifrado com sucesso!\n\n"
                f"Tamanho descompactado: {len(resultado_binario)} bytes\n\n"
                f"Clica em 'Guardar Resultado' para salvar o ficheiro decifrado."
            )

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def guardar_resultado_aes(self, ctx):
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

    def update_ui_validation(self, ctx, ok, mensagens):
        """Habilita/desabilita botões e realça campos inválidos com base nas mensagens de validação."""
        # Habilitar/desabilitar botões
        try:
            if not ok:
                if "cifrar_btn" in ctx:
                    ctx["cifrar_btn"].config(state=tk.DISABLED)
                if "decifrar_btn" in ctx:
                    ctx["decifrar_btn"].config(state=tk.DISABLED)
            else:
                if "cifrar_btn" in ctx:
                    ctx["cifrar_btn"].config(state=tk.NORMAL)
                if "decifrar_btn" in ctx:
                    ctx["decifrar_btn"].config(state=tk.NORMAL)
        except Exception:
            pass

        # Tentar realçar campos inválidos (muda background se possível), e focar primeiro inválido
        invalid_keywords = ["inválid", "inválido", "erro", "vazio", "muito pequeno"]
        first_invalid_widget = None

        # Reset backgrounds first
        for key in ("tabela_entry", "chave_entry", "msg_entry", "entrada_entry"):
            if key in ctx:
                w = ctx[key]
                try:
                    w.config(bg='white')
                except Exception:
                    try:
                        w.configure(background='white')
                    except Exception:
                        pass

        for msg in mensagens:
            low = msg.lower()
            if any(k in low for k in invalid_keywords):
                # decide which widget to mark
                if "tabela" in low and "tabela_entry" in ctx:
                    bad = ctx["tabela_entry"]
                elif "chave aes" in low or "chave aes inválida" in low or "chave aes" in low or "chave des" in low or "chave inválida" in low or "chave des inválida" in low:
                    bad = ctx.get("chave_entry")
                elif "mensagem" in low or "mensagem inválida" in low or "criptograma" in low:
                    bad = ctx.get("msg_entry")
                elif "ficheiro de entrada" in low or "entrada" in low:
                    bad = ctx.get("entrada_entry")
                else:
                    bad = None

                if bad is not None:
                    try:
                        bad.config(bg='#ffdddd')
                    except Exception:
                        try:
                            bad.configure(background='#ffdddd')
                        except Exception:
                            pass
                    if first_invalid_widget is None:
                        first_invalid_widget = bad

        if first_invalid_widget is not None:
            try:
                first_invalid_widget.focus_set()
            except Exception:
                pass

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
