import socket

class SocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send_message(self, message: str):
        if not self.socket:
            return
        self.socket.send(message.encode())

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None