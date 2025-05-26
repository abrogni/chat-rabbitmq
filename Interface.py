# gui.py

import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from Cliente import ChatClient  # importa o cliente separado

class ChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat com RabbitMQ")

        self.username = simpledialog.askstring("Nome de usuário", "Digite seu nome de usuário:")
        if not self.username:
            messagebox.showerror("Erro", "Nome de usuário obrigatório.")
            root.quit()

        self.client = ChatClient(self.username, self.exibir_mensagem)

        self.txt_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20)
        self.txt_area.pack(padx=10, pady=5)
        self.txt_area.config(state=tk.DISABLED)

        self.group_frame = tk.Frame(root)
        self.group_frame.pack(padx=10, pady=5)

        self.group_entry = tk.Entry(self.group_frame)
        self.group_entry.pack(side=tk.LEFT)

        self.btn_add_group = tk.Button(self.group_frame, text="Entrar no grupo", command=self.add_group)
        self.btn_add_group.pack(side=tk.LEFT, padx=5)

        self.msg_entry = tk.Entry(root, width=60)
        self.msg_entry.pack(padx=10, pady=5)

        self.send_frame = tk.Frame(root)
        self.send_frame.pack()

        self.selected_group = tk.StringVar()
        self.group_menu = tk.OptionMenu(self.send_frame, self.selected_group, "")
        self.group_menu.pack(side=tk.LEFT)

        self.btn_send = tk.Button(self.send_frame, text="Enviar", command=self.send_message)
        self.btn_send.pack(side=tk.LEFT, padx=5)

    def add_group(self):
        group = self.group_entry.get().strip()
        if group:
            self.client.join_group(group)
            self.group_entry.delete(0, tk.END)
            self.update_group_menu(group)
            self.log(f"Você entrou no grupo '{group}'")

    def update_group_menu(self, group):
        menu = self.group_menu["menu"]
        menu.add_command(label=group, command=tk._setit(self.selected_group, group))
        if not self.selected_group.get():
            self.selected_group.set(group)

    def send_message(self):
        group = self.selected_group.get()
        msg = self.msg_entry.get().strip()
        if group and msg:
            self.client.send_message(group, msg)
            self.msg_entry.delete(0, tk.END)

    def exibir_mensagem(self, data):
        sender = data['sender']
        group = data['group']
        message = data['message']
        texto = f"[{group}] {sender}: {message}"

        self.txt_area.config(state=tk.NORMAL)
        self.txt_area.insert(tk.END, texto + "\n")
        self.txt_area.config(state=tk.DISABLED)
        self.txt_area.see(tk.END)

    def log(self, text):
        self.txt_area.config(state=tk.NORMAL)
        self.txt_area.insert(tk.END, f"* {text}\n")
        self.txt_area.config(state=tk.DISABLED)
        self.txt_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatGUI(root)
    root.mainloop()
