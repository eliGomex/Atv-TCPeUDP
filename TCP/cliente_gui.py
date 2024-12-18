import socket
import tkinter as tk
from tkinter import messagebox, scrolledtext


class ClienteTCPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente TCP")
        self.socket_cliente = None

        # Configuração da interface
        self.frame_top = tk.Frame(root)
        self.frame_top.pack(pady=10)

        self.label_host = tk.Label(self.frame_top, text="Servidor (IP):")
        self.label_host.grid(row=0, column=0, padx=5)

        self.entry_host = tk.Entry(self.frame_top, width=15)
        self.entry_host.grid(row=0, column=1, padx=5)
        self.entry_host.insert(0, "127.0.0.1")

        self.label_port = tk.Label(self.frame_top, text="Porta:")
        self.label_port.grid(row=0, column=2, padx=5)

        self.entry_port = tk.Entry(self.frame_top, width=5)
        self.entry_port.grid(row=0, column=3, padx=5)
        self.entry_port.insert(0, "65432")

        self.button_conectar = tk.Button(self.frame_top, text="Conectar", command=self.conectar_ao_servidor)
        self.button_conectar.grid(row=0, column=4, padx=5)

        self.frame_middle = tk.Frame(root)
        self.frame_middle.pack(pady=10)

        self.label_mensagem = tk.Label(self.frame_middle, text="Mensagem:")
        self.label_mensagem.grid(row=0, column=0, padx=5)

        self.entry_mensagem = tk.Entry(self.frame_middle, width=50)
        self.entry_mensagem.grid(row=0, column=1, padx=5)

        self.button_enviar = tk.Button(self.frame_middle, text="Enviar", command=self.enviar_mensagem, state=tk.DISABLED)
        self.button_enviar.grid(row=0, column=2, padx=5)

        self.frame_bottom = tk.Frame(root)
        self.frame_bottom.pack(pady=10)

        self.text_respostas = scrolledtext.ScrolledText(self.frame_bottom, width=60, height=15)
        self.text_respostas.pack()

    def conectar_ao_servidor(self):
        """Conecta ao servidor TCP."""
        host = self.entry_host.get()
        try:
            port = int(self.entry_port.get())
            self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_cliente.connect((host, port))
            self.text_respostas.insert(tk.END, f"Conectado ao servidor {host}:{port}\n")
            self.button_enviar.config(state=tk.NORMAL)
            self.button_conectar.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao conectar ao servidor: {e}")

    def enviar_mensagem(self):
        """Envia uma mensagem ao servidor e exibe a resposta."""
        mensagem = self.entry_mensagem.get()
        if not mensagem.strip():
            messagebox.showwarning("Aviso", "Digite uma mensagem válida.")
            return

        try:
            # Envia a mensagem para o servidor
            self.socket_cliente.sendall(mensagem.encode('utf-8'))

            # Recebe a resposta do servidor
            resposta = self.socket_cliente.recv(1024).decode('utf-8')
            self.text_respostas.insert(tk.END, f"Enviado: {mensagem}\n")
            self.text_respostas.insert(tk.END, f"Resposta: {resposta}\n\n")
            self.text_respostas.see(tk.END)
            self.entry_mensagem.delete(0, tk.END)
        except Exception as e:
            self.text_respostas.insert(tk.END, f"Erro ao enviar mensagem: {e}\n")
            self.text_respostas.see(tk.END)

    def fechar_conexao(self):
        """Fecha a conexão ao encerrar o programa."""
        if self.socket_cliente:
            try:
                self.socket_cliente.close()
            except:
                pass


# Inicializa a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteTCPApp(root)

    # Garante que a conexão será fechada ao sair
    root.protocol("WM_DELETE_WINDOW", lambda: (app.fechar_conexao(), root.destroy()))

    root.mainloop()
