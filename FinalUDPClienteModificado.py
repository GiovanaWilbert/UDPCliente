import socket
import time
import random

# Define o endereço e a porta do sevidor
server_address = ('localhost', 6789)

# Cria um UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)  # Cria um  timeout para o socket

# O número de mensagens a serem enviadas
total_messages = 1000

# Lista de mensagens IDs
message_ids = list(range(1, total_messages + 1))
#Simulando mensagens fora de ordem
message_ids[8] = 11
message_ids[10] = 9
message_ids[996] = 999
message_ids[998] = 997
print (message_ids)

# Parâmetros de controle de congestionamento
cwnd = 1  # Congestionamento de window (inicialmente 1 mensagem)
ssthresh = 64  # Slow start threshold
timeout = 1.0  # Timeout duration
max_cwnd = 100  # Maximum congestion window size

# Função para lidar com o controle de congestionamento
def congestion_control(success):
    global cwnd, ssthresh
    if success:
        if cwnd < ssthresh:
            cwnd += 1  # fase Slow start
        else:
            cwnd = min(cwnd + 1 / cwnd, max_cwnd)  # Congestion avoidance phase
    else:
        ssthresh = max(1, cwnd // 2)
        cwnd = 1  # Reset congestion window to 1
        print("Timeout ocorreu, reduzindo congestion window")

# Função para assegura o envio da mensagem
def send_message_with_ack(message, message_id):
    while True:
        client_socket.sendto(message.encode(), server_address)
        try:
            ack, server = client_socket.recvfrom(1024)
            ack_id = int(ack.decode().split()[1])
            if ack_id == message_id:
                print(f"Resposta do sevidor: {ack.decode()}")
                congestion_control(success=True)
                break
        except socket.timeout:
            print(f"Sem ACK da mensagem {message_id}, reenviando")
            congestion_control(success=False)

# Envio de 1000 mensagens, incluindo algumas fora de ordem
for message_id in message_ids:
    message = f"{message_id} Message {message_id} from client"
    send_message_with_ack(message, message_id)
    time.sleep(0.01)  # Pequeno delay para impedir de sobrecarregar o sevidor

print("Cliente enviou  1000 messagens")
client_socket.close()
