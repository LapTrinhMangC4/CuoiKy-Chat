# Developer README

Hướng dẫn môi trường phát triển

1) Yêu cầu
- Node.js >= 14 hoặc Python 3.8+ (tùy phần frontend/backend).

2) Thiết lập nhanh
- Cài phụ thuộc frontend (nếu có): `npm install` hoặc `yarn install`
- Cài phụ thuộc backend (Python): `pip install -r requirements.txt`

3) Lệnh thường dùng
- Chạy dev frontend: `npm run dev` hoặc `npm start`
- Chạy backend: `python app.py` hoặc `flask run` (tùy framework)
- Kiểm tra lint: `npm run lint`

4) Debug & cấu hình
- Sử dụng file `.env` cho biến môi trường; không commit file này.
- Nếu cần DB local, thêm bước tạo DB và chạy migrations ở đây.

5) Ghi chú
- Thêm hướng dẫn Docker hoặc CI/CD nếu nhóm dùng.

## Chạy qua Cloudflare Tunnel (cloudflared)

Nếu muốn chạy server trên máy A và client trên máy B qua Internet mà không mở port, dùng `cloudflared` để tạo TCP tunnel:

1. Cài `cloudflared`: theo hướng dẫn https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation

2. Trên máy chạy server, khởi động server (ví dụ mặc định port 1234):

```powershell
python server.py --host 127.0.0.1 --port 1234 --cloudflared
```

`server.py` có tùy chọn `--cloudflared` để tự khởi động `cloudflared tunnel --url tcp://HOST:PORT` và in public URL (ví dụ `tcp://abcd.l4.cf.tunnel.com:12345`).

3. Trên máy client, kết nối tới URL public do `cloudflared` cung cấp:

```powershell
python client.py --url tcp://abcd.l4.cf.tunnel.com:12345 --username "Alice"
```

Hoặc truyền `--host` và `--port` trực tiếp nếu bạn có địa chỉ IP/port công khai.

Ghi chú: đảm bảo `cloudflared` đã cài và có quyền khởi tạo tunnel trên máy server.
