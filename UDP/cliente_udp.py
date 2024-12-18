import socket


def cliente_udp(host='127.0.0.1', porta=65432):
    """Cliente UDP para enviar mensagens ao servidor."""
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Cliente conectado ao servidor {host}:{porta}")

    try:
        while True:
            mensagem = input("\nDigite a mensagem para o servidor (ou 'sair' para encerrar): ").strip()
            if mensagem.lower() == "sair":
                print("Encerrando cliente.")
                break

            # Envia mensagem ao servidor
            socket_cliente.sendto(mensagem.encode('utf-8'), (host, porta))

            # Recebe resposta do servidor
            resposta, _ = socket_cliente.recvfrom(1024)
            print(f"Resposta do servidor: {resposta.decode('utf-8')}")
    except Exception as e:
        print(f"Erro no cliente UDP: {e}")
    finally:
        socket_cliente.close()


if __name__ == "__main__":
    cliente_udp()
