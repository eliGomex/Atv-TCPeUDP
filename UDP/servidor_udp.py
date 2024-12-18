import socket
import time

def iniciar_servidor_udp(host='127.0.0.1', porta=65433):
    """Servidor UDP que processa mensagens dos clientes."""
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_servidor.bind((host, porta))
    print(f"Servidor UDP iniciado em {host}:{porta}")

    try:
        while True:
            mensagem, endereco_cliente = socket_servidor.recvfrom(1024)
            mensagem = mensagem.decode('utf-8')
            print(f"Mensagem recebida de {endereco_cliente}: {mensagem}")

            if mensagem.startswith("UPPER:"):
                resposta = mensagem[6:].upper()
            elif mensagem.startswith("REVERSE:"):
                resposta = mensagem[8:][::-1]
            elif mensagem.startswith("CALC:"):
                try:
                    resposta = str(eval(mensagem[5:]))
                except Exception as e:
                    resposta = f"Erro ao calcular: {e}"
            elif mensagem == "PING":
                resposta = "PONG"
            elif mensagem == "TIME":
                resposta = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            else:
                resposta = "Comando inválido."

            socket_servidor.sendto(resposta.encode('utf-8'), endereco_cliente)
            print(f"Resposta enviada para {endereco_cliente}: {resposta}")
    except Exception as e:
        print(f"Erro no servidor UDP: {e}")
    finally:
        socket_servidor.close()

if __name__ == "__main__":
    iniciar_servidor_udp()
