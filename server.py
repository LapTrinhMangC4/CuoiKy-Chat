import socket
import threading
from datetime import datetime
import json
import argparse
import os

# Default bind address for the server. Keep localhost; ngrok will forward to this.
HOST = os.environ.get('CHAT_HOST', '127.0.0.1')
PORT = int(os.environ.get('CHAT_PORT', 1234))
BUFFER_SIZE = 1024
HISTORY_FILE = "chat_history.txt"

clients = {}  # {socket: {'username': 'Alice', 'avatar': '😀'}}
clients_lock = threading.Lock()

def broadcast(message, sender=None):
    """Gửi tin nhắn đến tất cả clients"""
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client)

def save_history(message):
    """Lưu lịch sử chat"""
    try:
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    except:
        pass

def remove_client(client):
    """Xóa client khi disconnect"""
    if client in clients:
        user_data = clients[client]
        username = user_data['username']
        avatar = user_data.get('avatar', '👤')
        
        del clients[client]
        print(f"❌ {avatar} {username} đã ngắt kết nối")
        
        # Thông báo user rời phòng
        timestamp = datetime.now().strftime("%H:%M:%S")
        leave_msg = json.dumps({
            'type': 'system',
            'message': f'{avatar} {username} đã rời khỏi phòng chat',
            'time': timestamp
        })
        broadcast(leave_msg)
        save_history(f"[{timestamp}] SYSTEM: {avatar} {username} đã rời khỏi phòng chat")
        
        send_user_list()

def send_user_list():
    """Gửi danh sách users"""
    user_list = [
        {'username': data['username'], 'avatar': data.get('avatar', '👤')} 
        for data in clients.values()
    ]
    msg = json.dumps({
        'type': 'user_list',
        'users': user_list
    })
    broadcast(msg)

def handle_client(client):
    """Xử lý client"""
    username = None
    avatar = '👤'
    
    try:
        # Nhận username và avatar
        user_info = client.recv(1024).decode('utf-8')
        user_data = json.loads(user_info)
        username = user_data['username']
        avatar = user_data.get('avatar', '👤')
        
        clients[client] = {
            'username': username,
            'avatar': avatar
        }
        
        print(f"✅ {avatar} {username} đã kết nối từ {client.getpeername()}")
        
        # Thông báo user mới join
        timestamp = datetime.now().strftime("%H:%M:%S")
        join_msg = json.dumps({
            'type': 'system',
            'message': f'{avatar} {username} đã tham gia phòng chat',
            'time': timestamp
        })
        broadcast(join_msg, client)
        save_history(f"[{timestamp}] SYSTEM: {avatar} {username} đã tham gia phòng chat")
        
        send_user_list()
        
        # Lắng nghe tin nhắn
        while True:
            msg_data = client.recv(1024).decode('utf-8')
            if msg_data:
                data = json.loads(msg_data)
                
                if data['type'] == 'message':
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    full_msg = json.dumps({
                        'type': 'message',
                        'username': username,
                        'avatar': avatar,
                        'message': data['message'],
                        'time': timestamp
                    })
                    
                    print(f"[{timestamp}] {avatar} {username}: {data['message']}")
                    save_history(f"[{timestamp}] {avatar} {username}: {data['message']}")
                    
                    # Gửi lại cho sender và broadcast
                    client.send(full_msg.encode('utf-8'))
                    broadcast(full_msg, client)
            else:
                break
                
    except Exception as e:
        print(f"⚠️ Lỗi: {e}")
    finally:
        if client in clients:
            remove_client(client)
        client.close()

def main():
    """Khởi động server"""
    parser = argparse.ArgumentParser(description='Run chat server (optionally with ngrok)')
    parser.add_argument('--host', default=HOST, help='Host to bind (default: %(default)s)')
    parser.add_argument('--port', type=int, default=PORT, help='Port to bind (default: %(default)s)')
    parser.add_argument('--ngrok', action='store_true', help='Start an ngrok TCP tunnel and print public address')
    args = parser.parse_args()

    bind_host = args.host
    bind_port = args.port

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((bind_host, bind_port))
    server.listen(5)

    # Optionally start ngrok TCP tunnel and print public URL
    if args.ngrok:
        try:
            from pyngrok import ngrok

            # Start a TCP tunnel that forwards to bind_port
            tunnel = ngrok.connect(bind_port, "tcp")
            public_url = tunnel.public_url  # like tcp://0.tcp.ngrok.io:XXXXX
            print("\n🔗 Ngrok tunnel started:", public_url)
            print("Use the host and port from the tcp URL on remote clients (example: 0.tcp.ngrok.io:XXXXX)\n")
        except Exception as e:
            print(f"⚠️ Không thể khởi động ngrok: {e}")
            print("Tiếp tục chạy server cục bộ...\n")

    print("=" * 60)
    print("🚀 SERVER CHAT VỚI AVATAR ĐANG CHẠY")
    print("=" * 60)
    print(f"📍 Host: {bind_host}")
    print(f"🔌 Port: {bind_port}")
    print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("✨ Tính năng: Hỗ trợ avatar cho mỗi user")
    print("Đang chờ kết nối...\n")

    try:
        while True:
            client, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(client,))
            thread.daemon = True
            thread.start()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server đang tắt...")
        server.close()

if __name__ == "__main__":
    main()