import websocket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
from datetime import datetime

WS_URL = "wss://born-prepared-sussex-labour.trycloudflare.com"


class ChatClient:
    def __init__(self):
        self.ws = None
        self.username = ""
        self.avatar = "👤"
        self.icon_library = {
            '😊 Biểu cảm': [
                '😀', '😃', '😄', '😁', '😆', '😅', '🤣', '😂',
                '🙂', '🙃', '😉', '😊', '😇', '🥰', '😍', '🤩',
                '😘', '😗', '😚', '😙', '😋', '😛', '😜', '🤪',
                '😝', '🤑', '🤗', '🤭', '🤫', '🤔', '🤐', '🤨',
                '😐', '😑', '😶', '😏', '😒', '🙄', '😬', '🤥',
                '😌', '😔', '😪', '🤤', '😴', '😷', '🤒', '🤕'
            ],
            '❤️ Cảm xúc': [
                '😢', '😭', '😤', '😠', '😡', '🤬', '😱', '😨',
                '😰', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥',
                '😈', '👿', '💀', '☠️', '💩', '🤡', '👹', '👺',
                '👻', '👽', '👾', '🤖', '😺', '😸', '😹', '😻',
                '😼', '😽', '🙀', '😿', '😾', '❤️', '🧡', '💛',
                '💚', '💙', '💜', '🖤', '🤍', '🤎', '💔', '❣️'
            ],
            '👋 Cử chỉ': [
                '👋', '🤚', '🖐️', '✋', '🖖', '👌', '🤏', '✌️',
                '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆', '🖕',
                '👇', '☝️', '👍', '👎', '✊', '👊', '🤛', '🤜',
                '👏', '🙌', '👐', '🤲', '🤝', '🙏', '✍️', '💅',
                '🤳', '💪', '🦾', '🦿', '🦵', '🦶', '👂', '🦻',
                '👃', '🧠', '🦷', '🦴', '👀', '👁️', '👅', '👄'
            ],
            '🐶 Động vật': [
                '🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼',
                '🐨', '🐯', '🦁', '🐮', '🐷', '🐸', '🐵', '🙈',
                '🙉', '🙊', '🐔', '🐧', '🐦', '🐤', '🐣', '🐥',
                '🦆', '🦅', '🦉', '🦇', '🐺', '🐗', '🐴', '🦄',
                '🐝', '🐛', '🦋', '🐌', '🐞', '🐜', '🦟', '🦗',
                '🕷️', '🦂', '🐢', '🐍', '🦎', '🦖', '🦕', '🐙'
            ],
            '🍕 Đồ ăn': [
                '🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇',
                '🍓', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝',
                '🍅', '🍆', '🥑', '🥦', '🥬', '🥒', '🌶️', '🌽',
                '🥕', '🧄', '🧅', '🥔', '🍠', '🥐', '🥯', '🍞',
                '🥖', '🥨', '🧀', '🥚', '🍳', '🧈', '🥞', '🧇',
                '🥓', '🥩', '🍗', '🍖', '🦴', '🌭', '🍔', '🍟'
            ],
            '⚽ Thể thao': [
                '⚽', '🏀', '🏈', '⚾', '🥎', '🎾', '🏐', '🏉',
                '🥏', '🎱', '🪀', '🏓', '🏸', '🏒', '🏑', '🥍',
                '🏏', '🥅', '⛳', '🪁', '🏹', '🎣', '🤿', '🥊',
                '🥋', '🎽', '🛹', '🛼', '🛷', '⛸️', '🥌', '🎿',
                '⛷️', '🏂', '🪂', '🏋️', '🤼', '🤸', '🤺', '⛹️',
                '🤾', '🏌️', '🏇', '🧘', '🏊', '🤽', '🚣', '🧗'
            ],
            '🚗 Phương tiện': [
                '🚗', '🚕', '🚙', '🚌', '🚎', '🏎️', '🚓', '🚑',
                '🚒', '🚐', '🚚', '🚛', '🚜', '🦯', '🦽', '🦼',
                '🛴', '🚲', '🛵', '🏍️', '🛺', '🚨', '🚔', '🚍',
                '🚘', '🚖', '🚡', '🚠', '🚟', '🚃', '🚋', '🚞',
                '🚝', '🚄', '🚅', '🚈', '🚂', '🚆', '🚇', '🚊',
                '🚉', '✈️', '🛫', '🛬', '🛩️', '💺', '🚁', '🛰️'
            ],
            '⭐ Biểu tượng': [
                '⭐', '🌟', '✨', '💫', '🔥', '💥', '💢', '💨',
                '💦', '💧', '💤', '💨', '🌈', '☀️', '⛅', '☁️',
                '🌤️', '⛈️', '🌩️', '⚡', '❄️', '☃️', '⛄', '☄️',
                '💎', '💍', '👑', '🎯', '🎮', '🎲', '🎰', '🎳',
                '🎨', '🎭', '🎪', '🎬', '🎤', '🎧', '🎼', '🎹',
                '🥁', '🎷', '🎺', '🎸', '🪕', '🎻', '🎲', '♟️'
            ],
            '🏠 Vật dụng': [
                '🏠', '🏡', '🏢', '🏣', '🏤', '🏥', '🏦', '🏨',
                '🏩', '🏪', '🏫', '🏬', '🏭', '🏯', '🏰', '💒',
                '🗼', '🗽', '⛪', '🕌', '🛕', '🕍', '⛩️', '🕋',
                '📱', '💻', '⌨️', '🖥️', '🖨️', '🖱️', '🖲️', '🕹️',
                '💽', '💾', '💿', '📀', '📼', '📷', '📸', '📹',
                '🎥', '📞', '☎️', '📟', '📠', '📺', '📻', '🎙️'
            ]
        }

        self.avatar_options = ['👤', '😀', '😎', '🤓', '🥳', '🤩', '😇', '🤠', 
                               '👨', '👩', '👦', '👧', '🧑', '👶', '🐶', '🐱',
                               '🦊', '🐼', '🐨', '🦁', '🐯', '🐸', '🐵', '🦄']

        self.window = tk.Tk()
        self.window.title("💬 Chat Application")
        self.window.geometry("950x800")
        self.window.configure(bg='#F0F4F8')

        self.setup_login_screen()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    # ================= LOGIN =================
    def setup_login_screen(self):
        self.login_frame = tk.Frame(self.window, bg='#F0F4F8')
        self.login_frame.pack(expand=True, fill='both')
        
        container = tk.Frame(self.login_frame, bg='white', bd=0, relief='flat')
        container.place(relx=0.5, rely=0.5, anchor='center', width=450, height=400)
        
        shadow_frame = tk.Frame(self.login_frame, bg='#E0E7EF', bd=0)
        shadow_frame.place(relx=0.5, rely=0.5, anchor='center', width=454, height=404)
        container.lift()
        
        # Logo
        logo_label = tk.Label(container, text="💬", font=('Arial', 80), bg='white', fg='#3B82F6')
        logo_label.pack(pady=(50, 10))
        
        # Title
        title = tk.Label(container, text="CHAT APPLICATION", font=('Arial', 26, 'bold'), bg='white', fg='#1E293B')
        title.pack(pady=(0, 5))
        
        subtitle = tk.Label(container, text="Kết nối và trò chuyện", font=('Arial', 12), bg='white', fg='#64748B')
        subtitle.pack(pady=(0, 30))
        
        # Username input
        input_frame = tk.Frame(container, bg='white')
        input_frame.pack(pady=10, padx=50, fill='x')
        
        tk.Label(input_frame, text="👤 Tên của bạn", font=('Arial', 13, 'bold'), bg='white', fg='#1E293B', anchor='w').pack(fill='x', pady=(0, 8))
        
        entry_container = tk.Frame(input_frame, bg='#E0E7EF', bd=2)
        entry_container.pack(fill='x')
        
        self.username_entry = tk.Entry(entry_container, font=('Arial', 15), bg='white', fg='#1E293B', insertbackground='#3B82F6', relief='flat', bd=0)
        self.username_entry.pack(ipady=12, ipadx=10, fill='x')
        self.username_entry.bind('<Return>', lambda e: self.join_chat())
        self.username_entry.focus()
        
        # Join button
        self.join_btn = tk.Button(input_frame, text="🚀 Tham gia Chat", font=('Arial', 14, 'bold'), bg='#3B82F6', fg='white', activebackground='#2563EB', activeforeground='white', relief='flat', bd=0, cursor='hand2', command=self.join_chat)
        self.join_btn.pack(fill='x', ipady=14, pady=(20, 0))
        
        self.join_btn.bind('<Enter>', lambda e: self.join_btn.config(bg='#2563EB'))
        self.join_btn.bind('<Leave>', lambda e: self.join_btn.config(bg='#3B82F6'))
        

    # ================= CHAT UI =================
    def setup_chat_screen(self):
        """Màn hình chat"""
        self.login_frame.destroy()
        
        main_container = tk.Frame(self.window, bg='#F0F4F8')
        main_container.pack(expand=True, fill='both')
        
        # ===== HEADER =====
        header = tk.Frame(main_container, bg='#3B82F6', height=70)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        left_header = tk.Frame(header, bg='#3B82F6')
        left_header.pack(side='left', padx=25, pady=15)
        
        title_label = tk.Label(left_header, text="💬 Chat Room", font=('Arial', 20, 'bold'), bg='#3B82F6', fg='white')
        title_label.pack()
        
        right_header = tk.Frame(header, bg='#3B82F6')
        right_header.pack(side='right', padx=25, pady=15)
        
        online_container = tk.Frame(right_header, bg='white', bd=0)
        online_container.pack(side='left', padx=(0, 15))
        
        self.online_label = tk.Label(online_container, text="🟢 1 người online", font=('Arial', 11, 'bold'), bg='white', fg='#10B981', padx=12, pady=4)
        self.online_label.pack()
        
        self.user_label = tk.Label(right_header, text=f"👤 {self.username}", font=('Arial', 12), bg='#3B82F6', fg='white')
        self.user_label.pack()
        
        # ===== MAIN CONTENT =====
        content_frame = tk.Frame(main_container, bg='#F0F4F8')
        content_frame.pack(expand=True, fill='both', padx=15, pady=15)
        
        # Chat messages container
        chat_container = tk.Frame(content_frame, bg='#E0E7EF', bd=2)
        chat_container.pack(expand=True, fill='both', pady=(0, 10))
        
        self.text_area = scrolledtext.ScrolledText(chat_container, wrap=tk.WORD, font=('Arial', 12), bg='white', fg='#1E293B', insertbackground='#3B82F6', relief='flat', bd=0, state='disabled', padx=15, pady=15)
        self.text_area.pack(expand=True, fill='both')
        
        # Tags cho styling
        self.text_area.tag_config('system', foreground='#8B5CF6', font=('Arial', 11, 'italic'), justify='center')
        self.text_area.tag_config('username', foreground='#3B82F6', font=('Arial', 12, 'bold'))
        self.text_area.tag_config('username_self', foreground='#10B981', font=('Arial', 12, 'bold'))
        self.text_area.tag_config('message', foreground='#1E293B', font=('Arial', 12))
        self.text_area.tag_config('time', foreground='#94A3B8', font=('Arial', 10))
        self.text_area.tag_config('avatar', font=('Arial', 14))
        
        # ===== INPUT AREA =====
        input_container = tk.Frame(content_frame, bg='white', bd=2, relief='flat')
        input_container.pack(fill='x')
        
        input_inner = tk.Frame(input_container, bg='white')
        input_inner.pack(fill='x', padx=10, pady=10)
        
        # Icon library button
        icon_btn = tk.Button(input_inner, text="📚", font=('Arial', 18), bg='#8B5CF6', fg='white', activebackground='#7C3AED', activeforeground='white', relief='flat', bd=0, cursor='hand2', command=self.open_icon_library, width=3)
        icon_btn.pack(side='left', padx=(0, 5))
        icon_btn.bind('<Enter>', lambda e: icon_btn.config(bg='#7C3AED'))
        icon_btn.bind('<Leave>', lambda e: icon_btn.config(bg='#8B5CF6'))
        
        # Message input
        entry_frame = tk.Frame(input_inner, bg='#E0E7EF', bd=2)
        entry_frame.pack(side='left', expand=True, fill='x', padx=(0, 10))
        
        self.msg_entry = tk.Entry(entry_frame, font=('Arial', 13), bg='white', fg='#1E293B', insertbackground='#3B82F6', relief='flat', bd=0)
        self.msg_entry.pack(fill='x', ipady=12, ipadx=10)
        self.msg_entry.bind('<Return>', lambda e: self.send_message())
        self.msg_entry.focus()
        
        # Send button
        self.send_btn = tk.Button(input_inner, text="📤 Gửi", font=('Arial', 13, 'bold'), bg='#10B981', fg='white', activebackground='#059669', activeforeground='white', relief='flat', bd=0, cursor='hand2', command=self.send_message, padx=30, pady=12)
        self.send_btn.pack(side='right')
        
        self.send_btn.bind('<Enter>', lambda e: self.send_btn.config(bg='#059669'))
        self.send_btn.bind('<Leave>', lambda e: self.send_btn.config(bg='#10B981'))
        
    def open_icon_library(self):
        """Mở thư viện icon"""
        library_window = tk.Toplevel(self.window)
        library_window.title("📚 Thư Viện Icon")
        library_window.geometry("750x650")
        library_window.configure(bg='white')
        library_window.transient(self.window)
        library_window.grab_set()
        
        # Title
        title = tk.Label(library_window, text="📚 Chọn Icon Để Chèn Vào Tin Nhắn", font=('Arial', 18, 'bold'), bg='white', fg='#1E293B')
        title.pack(pady=15)
        
        # Close button
        close_btn = tk.Button(library_window, text="✖ Đóng", font=('Arial', 11, 'bold'), bg='#EF4444', fg='white', activebackground='#DC2626', relief='flat', bd=0, cursor='hand2', command=library_window.destroy)
        close_btn.pack(pady=(0, 10))
        close_btn.bind('<Enter>', lambda e: close_btn.config(bg='#DC2626'))
        close_btn.bind('<Leave>', lambda e: close_btn.config(bg='#EF4444'))
        
        # Content area với scroll
        canvas = tk.Canvas(library_window, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(library_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Hiển thị icons theo category
        for category, icons in self.icon_library.items():
            # Category header
            cat_label = tk.Label(scrollable_frame, text=category, font=('Arial', 14, 'bold'), bg='white', fg='#1E293B', anchor='w')
            cat_label.pack(fill='x', padx=20, pady=(15, 10))
            
            # Icons grid
            icon_frame = tk.Frame(scrollable_frame, bg='white')
            icon_frame.pack(fill='x', padx=20, pady=(0, 10))
            
            row = 0
            col = 0
            max_cols = 14
            
            for icon in icons:
                btn = tk.Button(icon_frame, text=icon, font=('Arial', 20), bg='#F0F4F8', fg='#1E293B', relief='flat', bd=0, cursor='hand2', width=2, height=1, command=lambda i=icon, w=library_window: [self.insert_icon(i), w.destroy()])
                btn.grid(row=row, column=col, padx=3, pady=3)
                
                btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#E0E7EF'))
                btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#F0F4F8'))
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
            
            # Separator
            sep = tk.Frame(scrollable_frame, bg='#E0E7EF', height=1)
            sep.pack(fill='x', padx=20, pady=5)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=(0, 10))
        scrollbar.pack(side="right", fill="y", pady=(0, 10))
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def insert_icon(self, icon):
        """Chèn icon vào ô nhập tin nhắn"""
        current_pos = self.msg_entry.index(tk.INSERT)
        self.msg_entry.insert(current_pos, icon)
        self.msg_entry.focus()
        
    # ================= WEBSOCKET =================
    def join_chat(self):
        name = self.username_entry.get().strip()
        if not name:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên")
            return

        self.username = name

        self.ws = websocket.WebSocketApp(
            WS_URL,
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_ws_close
        )

        threading.Thread(
            target=self.ws.run_forever,
            daemon=True
        ).start()

        self.setup_chat_screen()

    def on_open(self, ws):
        ws.send(json.dumps({
            "type": "join",
            "username": self.username,
            "avatar": self.avatar
        }))

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
        except:
            return

        self.window.after(0, self.handle_message, data)

        if data['type'] == 'system':
            self.text_area.insert(
                tk.END,
                f"\n⚠ {data['message']}\n"
            )

        elif data['type'] == 'message':
            self.text_area.insert(
                tk.END,
                f"[{data['time']}] {data['avatar']} {data['username']}: {data['message']}\n"
            )

        self.text_area.config(state='disabled')
        self.text_area.see(tk.END)

    def handle_message(self, data):
        self.text_area.config(state='normal')

        if data['type'] == 'system':
            self.text_area.insert(
                tk.END,
                f"\n⚠ {data['message']}\n",
                'system'
            )
        elif data['type'] == 'message':
            self.text_area.insert(
                tk.END,
                f"[{data['time']}] ",
                'time'
            )
            self.text_area.insert(
                tk.END,
                f"{data['avatar']} {data['username']}: ",
                'username'
            )
            self.text_area.insert(
                tk.END,
                f"{data['message']}\n",
                'message'
            )

        elif data['type'] == 'user_list':
            count = data.get('count', 1)
            self.online_label.config(
                text=f"🟢 {count} người online"
            )
        self.text_area.config(state='disabled')
        self.text_area.see(tk.END)

    def send_message(self):
        msg = self.msg_entry.get().strip()
        if not msg:
            return

        self.ws.send(json.dumps({
            "type": "message",
            "message": msg
        }))
        self.msg_entry.delete(0, tk.END)

    def on_ws_close(self, ws, *args):
        messagebox.showinfo("Mất kết nối", "Server đã đóng")

    def on_close(self):
        try:
            if self.ws:
                self.ws.close()
        except:
            pass
        self.window.destroy()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    ChatClient().run()
