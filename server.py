import socket

HOST = '127.0.0.1'
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Server đang chạy...")

client, addr = server.accept()
print("Client kết nối từ", addr)

while True:
    msg = client.recv(1024).decode()
    if not msg:
        break
    print("Client:", msg)

client.close()
server.close()
