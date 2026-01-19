import socket
import threading
import json
import tkinter as tk
from tkinter import messagebox

from utils.constants import HOST, PORT
from ui.login import LoginScreen
from ui.chat_screen import ChatScreen
from network.receiver import Receiver

class ChatClient:
    def __init__(self):
        self.client = None
        self.username = ""
        self.avatar = "👤"
        self.running = True

        self.window = tk.Tk()
        self.window.title("💬 Chat Application")
        self.window.geometry("950x800")

        self.login_screen = LoginScreen(self)

    def connect_server(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((HOST, PORT))

            user_data = json.dumps({
                "username": self.username,
                "avatar": self.avatar
            })
            self.client.send(user_data.encode())

            ChatScreen(self)

            Receiver(self).start()

        except Exception as e:
            messagebox.showerror("Lỗi kết nối", str(e))

    def run(self):
        self.window.mainloop()
