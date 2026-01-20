import tkinter as tk

class ChatScreen:
    def __init__(self, app):
        self.app = app

        self.frame = tk.Frame(app.window)
        self.frame.pack(fill=tk.BOTH, expand=True)

        title = tk.Label(self.frame, text="Phòng chat", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        self.messages_frame = tk.Frame(self.frame)
        self.messages_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.messages_listbox = tk.Listbox(
            self.messages_frame,
            font=("Arial", 12)
        )
        self.messages_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.messages_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.messages_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.messages_listbox.yview)

        input_frame = tk.Frame(self.frame)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        self.entry_message = tk.Entry(input_frame, font=("Arial", 12))
        self.entry_message.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entry_message.bind("<Return>", lambda e: self.send_message())

        send_button = tk.Button(input_frame, text="Gửi", command=self.send_message)
        send_button.pack(side=tk.RIGHT)

    def send_message(self):
        text = self.entry_message.get().strip()
        if not text:
            return

        display_text = f"{self.app.username}: {text}"
        self.messages_listbox.insert(tk.END, display_text)
        self.messages_listbox.see(tk.END)

        self.entry_message.delete(0, tk.END)