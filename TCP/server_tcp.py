import socket
import threading
import time

# Estatísticas do servidor
clientes_conectados = 0
mensagens_processadas = 0
tempo_inicio_servidor = time.time()

def lidar_com_cliente(socket_cliente, endereco_cliente):
    """Lida com as mensagens do cliente."""
    global mensagens_processadas, clientes_conectados
    try:
        while True:
            mensagem = socket_cliente.recv(1024).decode('utf-8')
            if not mensagem:
                print(f"Cliente {endereco_cliente} desconectado.")
                break

            mensagens_processadas += 1
            print(f"Mensagem recebida de {endereco_cliente}: {mensagem}")

            if mensagem.startswith("invert "):
                texto_para_inverter = mensagem[7:]
                resposta = texto_para_inverter[::-1]
            elif mensagem.startswith("count "):
                texto_para_contar = mensagem[6:]
                resposta = str(len(texto_para_contar))
            elif mensagem.replace(" ", "").isdigit():
                try:
                    numeros = list(map(int, mensagem.split()))
                    resposta = str(sum(numeros))
                except ValueError:
                    resposta = "Erro: Entrada inválida para soma."
            else:
                resposta = "Comando inválido. Use 'invert <texto>', 'count <texto>' ou números separados por espaço."

            socket_cliente.send(resposta.encode('utf-8'))
            print(f"Resposta enviada para {endereco_cliente}: {resposta}")

    except Exception as e:
        print(f"Erro com o cliente {endereco_cliente}: {e}")
    finally:
        clientes_conectados -= 1
        socket_cliente.close()

def iniciar_servidor(host='127.0.0.1', porta=65432):
    """Inicializa o servidor TCP."""
    global clientes_conectados
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.bind((host, porta))
    socket_servidor.listen(5)
    print(f"Servidor TCP iniciado em {host}:{porta}")

    try:
        while True:
            socket_cliente, endereco_cliente = socket_servidor.accept()
            clientes_conectados += 1
            print(f"Cliente conectado: {endereco_cliente}")
            thread_cliente = threading.Thread(target=lidar_com_cliente, args=(socket_cliente, endereco_cliente))
            thread_cliente.start()
    except KeyboardInterrupt:
        print("\nServidor finalizado pelo usuário.")
    except Exception as e:
        print(f"Erro no servidor: {e}")
    finally:
        socket_servidor.close()

def exibir_estatisticas():
    """Exibe estatísticas do servidor periodicamente."""
    global tempo_inicio_servidor
    while True:
        time.sleep(10)  # Atualiza as estatísticas a cada 10 segundos
        tempo_atividade = time.time() - tempo_inicio_servidor
        print("\n=== Estatísticas do Servidor ===")
        print(f"Clientes conectados atualmente: {clientes_conectados}")
        print(f"Mensagens processadas: {mensagens_processadas}")
        print(f"Tempo de atividade: {tempo_atividade:.2f} segundos\n")

if __name__ == "__main__":
    thread_estatisticas = threading.Thread(target=exibir_estatisticas, daemon=True)
    thread_estatisticas.start()
    iniciar_servidor()
