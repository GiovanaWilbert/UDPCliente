import socket
import random

# Define o endereço e a porta do sevidor
server_address = ('localhost', 6789)

# Cria um UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Vincula o socket ao sevidor
server_socket.bind(server_address)

print("UDP aguardando mensagens...")

# Contador de mensagens
expected_message_id = 1
received_messages = {}

# Probabilidade de perda de pacote para simular perda de mensagens ou congestionamento
probability_congestion = 0.05
probability_loss = 0.05


def simulate_congestion():
    """Simula congestonamento por perda de pacote aleatória"""
    return random.random() < probability_congestion


def simulate_loss():
    """Simula perda de mensagen"""
    return random.random() < probability_loss


# Espera por datagrams
while expected_message_id <= 1000:
    message, client_address = server_socket.recvfrom(1024)
    if simulate_congestion():
        print(f"Pacote de {client_address} perdido mensagem {message_id+1} para simular congestionamento")
        continue

    if simulate_loss():
        print(f"Pacote de  {client_address} perdido mensagem {message_id+1} para simular perda de mensagem")
        continue

    message_id, msg = message.decode().split(" ", 1)
    message_id = int(message_id)

    if message_id == expected_message_id:
        print(f"Message {message_id} from {client_address}: {msg}")
        expected_message_id += 1

        while expected_message_id in received_messages:
            print(f"Mesagem {expected_message_id}  do {client_address}: {received_messages.pop(expected_message_id)}")
            expected_message_id += 1
    else:
        received_messages[message_id] = msg
        print(f"Menssagem fora de ordem {message_id} stored")

    # Enviar um acknowledgment de volta para o servidor
    ack = f"ACK {message_id}"
    server_socket.sendto(ack.encode(), client_address)

print("Servidor recebeu 1000 mensagens")
server_socket.close()