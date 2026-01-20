import socket
import threading

clients = []

def handle_client(client):
    while True:
        msg = client.recv(1024).decode()
        if not msg:
            break
        print(msg)
    clients.remove(client)
    client.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 1234))
server.listen()

print("Server multi-client đang chạy...")

while True:
    client, addr = server.accept()
    clients.append(client)
    threading.Thread(target=handle_client, args=(client,)).start()


def broadcast(message, sender):
    for c in clients:
        if c != sender:
            c.send(message.encode())
broadcast(msg, client)
