"""
CHAT CLIENT - Lập trình Mạng
Sử dụng: Socket TCP + Threading để nhận tin nhắn
Kết nối đến server để chat
"""

import socket
import threading
import sys

# Cấu hình kết nối
HOST = '127.0.0.1'  # Server address
PORT = 5555         # Server port

# Biến toàn cục
running = True
username = ""

def receive_messages(client_socket):
    """
    Thread nhận tin nhắn từ server
    
    Args:
        client_socket: Socket kết nối đến server
    """
    global running
    
    while running:
        try:
            # Nhận tin nhắn từ server
            message = client_socket.recv(1024).decode('utf-8')
            
            if not message:
                print("\n[ERROR] Mất kết nối với server")
                running = False
                break
            
            # Xử lý yêu cầu username từ server
            if message == "USERNAME":
                continue
            
            # Hiển thị tin nhắn
            print(f"\r{message}")
            print(f"[{username}] ", end='', flush=True)
            
        except Exception as e:
            if running:  # Chỉ hiển thị lỗi nếu vẫn đang chạy
                print(f"\n[ERROR] Lỗi nhận tin nhắn: {e}")
            running = False
            break

def send_messages(client_socket):
    """
    Thread gửi tin nhắn đến server
    
    Args:
        client_socket: Socket kết nối đến server
    """
    global running
    
    while running:
        try:
            # Hiển thị prompt
            message = input(f"[{username}] ")
            
            if not running:
                break
            
            if message.strip():
                # Gửi tin nhắn đến server
                client_socket.send(message.encode('utf-8'))
                
                # Xử lý lệnh quit
                if message.strip().lower() == '/quit':
                    print("\n[INFO] Đang ngắt kết nối...")
                    running = False
                    break
        
        except EOFError:
            # Xử lý Ctrl+D
            running = False
            break
        except KeyboardInterrupt:
            # Xử lý Ctrl+C
            running = False
            break
        except Exception as e:
            if running:
                print(f"\n[ERROR] Lỗi gửi tin nhắn: {e}")
            running = False
            break

def connect_to_server():
    """
    Kết nối đến chat server
    """
    global username, running
    
    # Bước 1: Tạo socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print(f"\n[CONNECTING] Đang kết nối đến {HOST}:{PORT}...")
        
        # Bước 2: Kết nối đến server
        client_socket.connect((HOST, PORT))
        print(f"[CONNECTED] Đã kết nối thành công!\n")
        
        # Bước 3: Chờ yêu cầu username từ server
        request = client_socket.recv(1024).decode('utf-8')
        
        if request == "USERNAME":
            # Nhập username
            while True:
                username = input("Nhập tên của bạn: ").strip()
                if username:
                    break
                print("[ERROR] Tên không được để trống!")
            
            # Gửi username đến server
            client_socket.send(username.encode('utf-8'))
        
        # Bước 4: Nhận thông báo chào mừng
        welcome = client_socket.recv(1024).decode('utf-8')
        print(welcome)
        
        # Hiển thị hướng dẫn
        print("""
╔══════════════════════════════════════════════════════════╗
║                    HƯỚNG DẪN SỬ DỤNG                    ║
╠══════════════════════════════════════════════════════════╣
║  /users  - Xem danh sách người dùng online              ║
║  /help   - Xem hướng dẫn                                ║
║  /quit   - Thoát khỏi chat                              ║
╚══════════════════════════════════════════════════════════╝
        """)
        
        # Bước 5: Tạo thread nhận tin nhắn
        receive_thread = threading.Thread(
            target=receive_messages,
            args=(client_socket,),
            daemon=True
        )
        receive_thread.start()
        
        # Bước 6: Thread chính xử lý gửi tin nhắn
        send_messages(client_socket)
        
    except ConnectionRefusedError:
        print(f"[ERROR] Không thể kết nối đến server {HOST}:{PORT}")
        print("[INFO] Hãy chắc chắn server đang chạy!")
    except Exception as e:
        print(f"[ERROR] Lỗi: {e}")
    finally:
        running = False
        print("\n[DISCONNECTED] Đã ngắt kết nối")
        try:
            client_socket.close()
        except:
            pass

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║           CHAT CLIENT - LẬP TRÌNH MẠNG                  ║
║           Socket TCP + Threading                         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        connect_to_server()
    except KeyboardInterrupt:
        print("\n[EXIT] Tạm biệt!")
        sys.exit(0)
