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
