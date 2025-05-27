import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from Usuario import Usuario
from datetime import datetime

class Chat:
    def __init__(self,tela_chat):
        self.tela_chat = tela_chat
        self.tela_chat.title("Chat")

        self.nome = simpledialog.askstring("Nome de usuário", "Digite seu nome de usuário:")
        if not self.nome:
            messagebox.showerror("Erro", "Nome de usuário obrigatório.")
            tela_chat.quit()
        
        self.usuario = Usuario(self.nome, self.exibir_mensagem)
        
        self.area_txt = scrolledtext.ScrolledText(tela_chat, wrap=tk.WORD, height=20)
        self.area_txt.pack(padx=10, pady=5)
        self.area_txt.config(state=tk.DISABLED)

        self.frame_grupo = tk.Frame(tela_chat)
        self.frame_grupo.pack(padx=10, pady=5)

        self.edit_grupo = tk.Entry(self.frame_grupo)
        self.edit_grupo.pack(side=tk.LEFT)

        self.bt_grupo = tk.Button(self.frame_grupo, text="Entrar no grupo", command=self.add_grupo)
        self.bt_grupo.pack(side=tk.LEFT, padx=5)

        self.bt_sair_grupo = tk.Button(self.frame_grupo, text="Sair do grupo", command=self.sair_grupo)
        self.bt_sair_grupo.pack(side=tk.LEFT, padx=5)

        self.edit_msg = tk.Entry(tela_chat, width=60)
        self.edit_msg.pack(padx=10, pady=5)

        self.frame_enviar = tk.Frame(tela_chat)
        self.frame_enviar.pack()

        self.selecao_grupo = tk.StringVar()
        self.combo_grupo = tk.OptionMenu(self.frame_enviar, self.selecao_grupo, "")
        self.combo_grupo.pack(side=tk.LEFT)

        self.bt_enviar = tk.Button(self.frame_enviar, text="Enviar", command=self.enviar_msg)
        self.bt_enviar.pack(side=tk.LEFT, padx=5)

    def add_grupo(self):
        grupo = self.edit_grupo.get().strip()
        if grupo:
            self.usuario.entrar_grupo(grupo)
            self.edit_grupo.delete(0, tk.END)
            self.update_combo_grupo(grupo)
            
            self.area_txt.config(state=tk.NORMAL)
            self.area_txt.insert(tk.END, f"Você entrou no grupo '{grupo}'\n")
            self.area_txt.config(state=tk.DISABLED)
            self.area_txt.see(tk.END)
        
    def update_combo_grupo(self, group):
        menu = self.combo_grupo["menu"]
        menu.add_command(label=group, command=tk._setit(self.selecao_grupo, group))
        if not self.selecao_grupo.get():
            self.selecao_grupo.set(group)
    
    def enviar_msg(self):
        grupo = self.selecao_grupo.get()
        msg = self.edit_msg.get().strip()
        if grupo and msg:
            self.usuario.enviar_msg(grupo, msg)
            self.edit_msg.delete(0, tk.END)
    
    def exibir_mensagem(self, dados):
        usuario = dados['usuario']
        grupo = dados['grupo']
        mensagem = dados['mensagem']
        hora = datetime.now().strftime("%H:%M:%S")
        texto = f"[{grupo}] {usuario}: {mensagem} \n {hora}"
        
        self.area_txt.config(state=tk.NORMAL)
        self.area_txt.insert(tk.END, texto + "\n")
        self.area_txt.config(state=tk.DISABLED)
        self.area_txt.see(tk.END)
    
    def sair_grupo(self):
        grupo = self.selecao_grupo.get()
        if grupo:
            self.usuario.sair_grupo(grupo)

            menu = self.combo_grupo["menu"]
            self.selecao_grupo.set("")
            menu.delete(grupo)

            self.area_txt.config(state=tk.NORMAL)
            self.area_txt.insert(tk.END, f"Você saiu do grupo '{grupo}'\n")
            self.area_txt.config(state=tk.DISABLED)
            self.area_txt.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = Chat(root)
    root.mainloop()
