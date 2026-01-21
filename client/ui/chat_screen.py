import tkinter as tk
from tkinter import scrolledtext
from ui.icon_library import ICON_LIBRARY

class ChatScreen:
    def __init__(self, app):
        self.app = app
        
        main_container = tk.Frame(app.window, bg='#F0F4F8')
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
        
        self.user_label = tk.Label(right_header, text=f"👤 {app.username}", font=('Arial', 12), bg='#3B82F6', fg='white')
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
        
        self.entry_message = tk.Entry(entry_frame, font=('Arial', 13), bg='white', fg='#1E293B', insertbackground='#3B82F6', relief='flat', bd=0)
        self.entry_message.pack(fill='x', ipady=12, ipadx=10)
        self.entry_message.bind('<Return>', lambda e: self.send_message())
        self.entry_message.focus()
        
        # Send button
        self.send_btn = tk.Button(input_inner, text="📤 Gửi", font=('Arial', 13, 'bold'), bg='#10B981', fg='white', activebackground='#059669', activeforeground='white', relief='flat', bd=0, cursor='hand2', command=self.send_message, padx=30, pady=12)
        self.send_btn.pack(side='right')
        
        self.send_btn.bind('<Enter>', lambda e: self.send_btn.config(bg='#059669'))
        self.send_btn.bind('<Leave>', lambda e: self.send_btn.config(bg='#10B981'))
    
    def open_icon_library(self):
        """Mở thư viện icon"""
        library_window = tk.Toplevel(self.app.window)
        library_window.title("📚 Thư Viện Icon")
        library_window.geometry("750x650")
        library_window.configure(bg='white')
        library_window.transient(self.app.window)
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
        for category, icons in ICON_LIBRARY.items():
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
        current_pos = self.entry_message.index(tk.INSERT)
        self.entry_message.insert(current_pos, icon)
        self.entry_message.focus()
    
    def send_message(self):
        """Gửi tin nhắn"""
        message = self.entry_message.get().strip()
        
        if message:
            try:
                import json
                msg_data = json.dumps({'type': 'message', 'message': message})
                self.app.client.send(msg_data.encode('utf-8'))
                self.entry_message.delete(0, tk.END)
            except Exception as e:
                from tkinter import messagebox
                messagebox.showerror("❌ Lỗi", f"Không thể gửi tin nhắn!\n{str(e)}")
    
    def display_message(self, data):
        """Hiển thị tin nhắn"""
        self.text_area.config(state='normal')
        
        if data['type'] == 'system':
            self.text_area.insert(tk.END, '\n')
            self.text_area.insert(tk.END, '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n', 'system')
            self.text_area.insert(tk.END, f"✨ {data['message']} ✨\n", 'system')
            self.text_area.insert(tk.END, '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n', 'system')
            
        elif data['type'] == 'message':
            is_self = data['username'] == self.app.username
            avatar = data.get('avatar', '👤')
            
            self.text_area.insert(tk.END, '\n')
            self.text_area.insert(tk.END, f"🕐 {data['time']}  ", 'time')
            
            self.text_area.insert(tk.END, f"{avatar} ", 'avatar')
            
            if is_self:
                self.text_area.insert(tk.END, f"{data['username']}\n", 'username_self')
            else:
                self.text_area.insert(tk.END, f"{data['username']}\n", 'username')
            
            self.text_area.insert(tk.END, f"   {data['message']}\n", 'message')
            
        elif data['type'] == 'user_list':
            user_count = len(data['users'])
            self.online_label.config(text=f"🟢 {user_count} người online")
        
        self.text_area.config(state='disabled')
        self.text_area.see(tk.END)
