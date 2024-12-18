import socket
import time


def lidar_com_cliente_udp(socket_servidor):
    """Função para lidar com mensagens de clientes UDP."""
    print("Servidor UDP aguardando mensagens...")
    try:
        while True:
            mensagem, endereco_cliente = socket_servidor.recvfrom(1024)
            mensagem = mensagem.decode('utf-8').strip()
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
                resposta = "Comando inválido. Use UPPER, REVERSE, CALC, PING ou TIME."

            # Enviar resposta ao cliente
            socket_servidor.sendto(resposta.encode('utf-8'), endereco_cliente)
            print(f"Resposta enviada para {endereco_cliente}: {resposta}")
    except Exception as e:
        print(f"Erro no servidor UDP: {e}")


def iniciar_servidor_udp(host='127.0.0.1', porta=65432):
    """Inicializa o servidor UDP."""
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_servidor.bind((host, porta))
    print(f"Servidor UDP iniciado em {host}:{porta}")

    try:
        lidar_com_cliente_udp(socket_servidor)
    except KeyboardInterrupt:
        print("\nServidor finalizado pelo usuário.")
    except Exception as e:
        print(f"Erro no servidor UDP: {e}")
    finally:
        socket_servidor.close()


if __name__ == "__main__":
    iniciar_servidor_udp()
