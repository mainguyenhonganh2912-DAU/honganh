# 🌐 HƯỚNG DẪN ĐƯA WEBSITE LÊN INTERNET TỰ ĐỘNG (DEPLOY SERVER)

Để đưa website **One Piece Figure Store** thành một trang web công khai trên Google (truy cập từ điện thoại, máy tính ở bất kỳ đâu), bạn có 3 lựa chọn cực kỳ đơn giản dưới đây:

---

## 🚀 CÁCH 1: DÙNG RENDER.COM (MIỄN PHÍ 100% - KHUYÊN DÙNG)

Render.com cho phép bạn có một trang web thực sự có tên miền HTTPS miễn phí (ví dụ: `https://onepiece-store.onrender.com`).

### 📌 Các bước thực hiện:

1. **Đưa code lên GitHub:**
   - Tạo một tài khoản trên [GitHub.com](https://github.com).
   - Tạo một Repository mới tên là `onepiece-figure-store`.
   - Đẩy toàn bộ thư mục dự án này lên GitHub.

2. **Kết nối Render.com:**
   - Đăng ký tài khoản miễn phí tại [Render.com](https://render.com).
   - Bấm nút **New +** -> Chọn **Web Service**.
   - Chọn **Connect GitHub** và chọn repository `onepiece-figure-store`.

3. **Render tự động phát hiện file `render.yaml`:**
   - Render sẽ tự động đọc file `render.yaml` đã được tạo sẵn trong dự án.
   - Bấm nút **Create Web Service**.
   - Chờ khoảng 2-3 phút, bạn sẽ có ngay đường link công khai dạng:
     👉 `https://onepiece-store.onrender.com`

---

## 🐍 CÁCH 2: DÙNG PYTHONANYWHERE.COM (MIỄN PHÍ DÀNH CHO DJANGO)

PythonAnywhere là trang chuyên chạy web Django miễn phí mà không cần thẻ tín dụng.

### 📌 Các bước thực hiện:

1. Đăng ký tài khoản tại [PythonAnywhere.com](https://www.pythonanywhere.com/).
2. Vào mục **Web** -> Bấm **Add a new web app**.
3. Chọn **Manual Configuration** -> Chọn **Python 3.11**.
4. Tải code của bạn lên hoặc dùng `git clone`.
5. Trong mục **WSGI configuration file**, trỏ tới file `du_an/wsgi.py`.
6. Bạn sẽ có ngay trang web với tên miền dạng:
   👉 `https://tencuaban.pythonanywhere.com`

---

## ⚡ CÁCH 3: XEM NHANH TRÊN MẠNG QUA NGROK (CHỈ MẤT 10 GIÂY)

Nếu bạn muốn gửi link cho bạn bè hoặc thầy cô xem ngay trang web đang chạy trên máy bạn:

1. Tải tool [Ngrok](https://ngrok.com/download) về máy.
2. Mở file `CHAY_WEBSITE.bat` trên máy bạn.
3. Mở Terminal và gõ lệnh:
   ```cmd
   ngrok http 8000
   ```
4. Ngrok sẽ cho bạn 1 đường link online dạng `https://xxxx.ngrok-free.app` để gửi cho bất kỳ ai truy cập trực tiếp vào máy bạn!

---

## 🛠️ CÁC FILE ĐÃ ĐƯỢC CHUẨN BỊ SẴN TRONG DỰ ÁN:

| File | Tác dụng |
|------|----------|
| `Procfile` | Khai báo lệnh chạy Gunicorn trên server Linux production |
| `render.yaml` | Cấu hình tự động cho Render.com |
| `Dockerfile` | Đóng gói Container Docker cho server chuyên nghiệp |
| `requirements.txt` | Danh sách các thư viện Python (Django, Gunicorn, Whitenoise...) |
| `du_an/settings.py` | Đã tích hợp **WhiteNoise** để tự động load file CSS, JS, Ảnh trên Server public |
