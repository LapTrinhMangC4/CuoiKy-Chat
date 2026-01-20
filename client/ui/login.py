import tkinter as tk
from tkinter import messagebox

class LoginScreen:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.window)
        self.frame.pack(expand=True)

        tk.Label(self.frame, text="CHAT APPLICATION", font=("Arial", 24, "bold")).pack(pady=20)

        self.entry = tk.Entry(self.frame, font=("Arial", 14))
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda e: self.join())

        tk.Button(self.frame, text="Tham gia", command=self.join).pack(pady=10)

    def join(self):
        username = self.entry.get().strip()
        if not username:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên")
            return

        self.app.username = username
        self.frame.destroy()
        self.app.connect_server()