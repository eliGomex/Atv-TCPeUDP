import socket
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk


class ClienteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente TCP/UDP")
        self.tcp_socket = None
        self.udp_socket = None

        # Configuração da interface
        self.notebook = ttk.Notebook(root)
        self.tcp_frame = tk.Frame(self.notebook)
        self.udp_frame = tk.Frame(self.notebook)

        self.notebook.add(self.tcp_frame, text="TCP")
        self.notebook.add(self.udp_frame, text="UDP")
        self.notebook.pack(expand=True, fill="both")

        # Configuração TCP
        self.setup_tcp_ui()

        # Configuração UDP
        self.setup_udp_ui()

    def setup_tcp_ui(self):
        """Configura a interface da aba TCP."""
        frame_top = tk.Frame(self.tcp_frame)
        frame_top.pack(pady=10)

        tk.Label(frame_top, text="Servidor (IP):").grid(row=0, column=0, padx=5)
        self.tcp_host_entry = tk.Entry(frame_top, width=15)
        self.tcp_host_entry.grid(row=0, column=1, padx=5)
        self.tcp_host_entry.insert(0, "127.0.0.1")

        tk.Label(frame_top, text="Porta:").grid(row=0, column=2, padx=5)
        self.tcp_port_entry = tk.Entry(frame_top, width=5)
        self.tcp_port_entry.grid(row=0, column=3, padx=5)
        self.tcp_port_entry.insert(0, "65432")

        self.tcp_connect_button = tk.Button(frame_top, text="Conectar", command=self.connect_tcp)
        self.tcp_connect_button.grid(row=0, column=4, padx=5)

        frame_middle = tk.Frame(self.tcp_frame)
        frame_middle.pack(pady=10)

        tk.Label(frame_middle, text="Mensagem:").grid(row=0, column=0, padx=5)
        self.tcp_message_entry = tk.Entry(frame_middle, width=50)
        self.tcp_message_entry.grid(row=0, column=1, padx=5)

        self.tcp_send_button = tk.Button(frame_middle, text="Enviar", command=self.send_tcp_message, state=tk.DISABLED)
        self.tcp_send_button.grid(row=0, column=2, padx=5)

        frame_bottom = tk.Frame(self.tcp_frame)
        frame_bottom.pack(pady=10)

        self.tcp_response_text = scrolledtext.ScrolledText(frame_bottom, width=60, height=15)
        self.tcp_response_text.pack()

    def setup_udp_ui(self):
        """Configura a interface da aba UDP."""
        frame_top = tk.Frame(self.udp_frame)
        frame_top.pack(pady=10)

        tk.Label(frame_top, text="Servidor (IP):").grid(row=0, column=0, padx=5)
        self.udp_host_entry = tk.Entry(frame_top, width=15)
        self.udp_host_entry.grid(row=0, column=1, padx=5)
        self.udp_host_entry.insert(0, "127.0.0.1")

        tk.Label(frame_top, text="Porta:").grid(row=0, column=2, padx=5)
        self.udp_port_entry = tk.Entry(frame_top, width=5)
        self.udp_port_entry.grid(row=0, column=3, padx=5)
        self.udp_port_entry.insert(0, "65433")

        self.udp_init_button = tk.Button(frame_top, text="Inicializar", command=self.init_udp)
        self.udp_init_button.grid(row=0, column=4, padx=5)

        frame_middle = tk.Frame(self.udp_frame)
        frame_middle.pack(pady=10)

        tk.Label(frame_middle, text="Mensagem:").grid(row=0, column=0, padx=5)
        self.udp_message_entry = tk.Entry(frame_middle, width=50)
        self.udp_message_entry.grid(row=0, column=1, padx=5)

        self.udp_send_button = tk.Button(frame_middle, text="Enviar", command=self.send_udp_message, state=tk.DISABLED)
        self.udp_send_button.grid(row=0, column=2, padx=5)

        frame_bottom = tk.Frame(self.udp_frame)
        frame_bottom.pack(pady=10)

        self.udp_response_text = scrolledtext.ScrolledText(frame_bottom, width=60, height=15)
        self.udp_response_text.pack()

    def connect_tcp(self):
        """Conecta ao servidor TCP."""
        host = self.tcp_host_entry.get()
        port = int(self.tcp_port_entry.get())
        try:
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.connect((host, port))
            self.tcp_response_text.insert(tk.END, f"Conectado ao servidor TCP {host}:{port}\n")
            self.tcp_send_button.config(state=tk.NORMAL)
            self.tcp_connect_button.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao conectar ao servidor TCP: {e}")

    def send_tcp_message(self):
        """Envia uma mensagem ao servidor TCP."""
        mensagem = self.tcp_message_entry.get()
        if not mensagem.strip():
            messagebox.showwarning("Aviso", "Digite uma mensagem válida.")
            return

        try:
            self.tcp_socket.sendall(mensagem.encode('utf-8'))
            resposta = self.tcp_socket.recv(1024).decode('utf-8')
            self.tcp_response_text.insert(tk.END, f"Enviado: {mensagem}\nResposta: {resposta}\n\n")
            self.tcp_response_text.see(tk.END)
        except Exception as e:
            self.tcp_response_text.insert(tk.END, f"Erro ao enviar mensagem TCP: {e}\n")

    def init_udp(self):
        """Inicializa o cliente UDP."""
        try:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_response_text.insert(tk.END, "Cliente UDP inicializado.\n")
            self.udp_send_button.config(state=tk.NORMAL)
            self.udp_init_button.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao inicializar o cliente UDP: {e}")

    def send_udp_message(self):
        """Envia uma mensagem ao servidor UDP."""
        mensagem = self.udp_message_entry.get()
        if not mensagem.strip():
            messagebox.showwarning("Aviso", "Digite uma mensagem válida.")
            return

        host = self.udp_host_entry.get()
        port = int(self.udp_port_entry.get())

        try:
            self.udp_socket.sendto(mensagem.encode('utf-8'), (host, port))
            resposta, _ = self.udp_socket.recvfrom(1024)  # Aguarda resposta do servidor
            self.udp_response_text.insert(tk.END, f"Enviado: {mensagem}\nResposta: {resposta.decode('utf-8')}\n\n")
            self.udp_response_text.see(tk.END)
        except Exception as e:
            self.udp_response_text.insert(tk.END, f"Erro ao enviar mensagem UDP: {e}\n")


    def close_sockets(self):
        """Fecha os sockets ao encerrar o programa."""
        if self.tcp_socket:
            self.tcp_socket.close()
        if self.udp_socket:
            self.udp_socket.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.close_sockets(), root.destroy()))
    root.mainloop()
