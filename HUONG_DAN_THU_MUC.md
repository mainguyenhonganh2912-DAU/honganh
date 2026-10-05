# 📂 HƯỚNG DẪN CẤU TRÚC THƯ MỤC DỰ ÁN
## One Piece Figure Store — Website Bán Mô Hình One Piece

> **Toàn bộ tên thư mục và file con được đặt bằng tiếng Việt** để dễ tìm code theo chức năng.

---

## 🗂️ CẤU TRÚC TỔNG QUAN

```
Mai Nguyễn Hồng Anh_24CT1/          ← Thư mục gốc dự án
│
├── du_an/                           ← ⚙️ CẤU HÌNH DỰ ÁN (Django project settings)
│   ├── settings.py                  ← Cài đặt toàn bộ dự án (database, static, templates...)
│   ├── urls.py                      ← URL gốc dự án (include sang cua_hang)
│   ├── wsgi.py                      ← Cổng kết nối web server (production)
│   └── asgi.py                      ← Cổng kết nối async web server
│
├── cua_hang/                        ← 🏪 ỨNG DỤNG CHÍNH (Django app)
│   ├── co_so_du_lieu.py             ← 🗄️ CƠ SỞ DỮ LIỆU: Tất cả Model (bảng DB)
│   ├── xu_ly_khach_hang.py          ← 🛒 XỬ LÝ KHÁCH HÀNG: Trang chủ, giỏ hàng, thanh toán
│   ├── xu_ly_tai_khoan.py           ← 🔐 XỬ LÝ TÀI KHOẢN: Đăng nhập, đăng ký, đăng xuất
│   ├── xu_ly_nguoi_ban.py           ← 🏪 XỬ LÝ NGƯỜI BÁN: Kênh người bán, quản lý sản phẩm
│   ├── xu_ly_quan_tri.py            ← 👑 XỬ LÝ QUẢN TRỊ: Cổng admin (thống kê, quản lý)
│   ├── duong_dan_url.py             ← 🔗 ĐƯỜNG DẪN URL: Toàn bộ URL patterns của app
│   ├── du_lieu_dung_chung.py        ← 🌐 DỮ LIỆU DÙNG CHUNG: Context processor (giỏ hàng, danh mục)
│   ├── trang_quan_tri_admin.py      ← 🛠️ TRANG QUẢN TRỊ ADMIN: Đăng ký model vào Django Admin
│   │
│   │   ── (File liên kết Django chuẩn — không cần sửa) ──
│   ├── models.py                    ← Import từ co_so_du_lieu.py
│   ├── views.py                     ← Import từ tất cả xu_ly_*.py
│   ├── urls.py                      ← Import từ duong_dan_url.py
│   ├── context_processors.py        ← Import từ du_lieu_dung_chung.py
│   ├── admin.py                     ← Import từ trang_quan_tri_admin.py
│   │
│   ├── apps.py                      ← Cấu hình app (label='shops' — GIỮ NGUYÊN!)
│   └── migrations/                  ← Lịch sử thay đổi database (tự động tạo)
│
├── giao_dien/                       ← 🎨 GIAO DIỆN (HTML Templates)
│   ├── base.html                    ← Khung chính (navbar, footer dùng chung)
│   └── cua_hang/                    ← Templates của app cua_hang
│       ├── trang_chu.html           ← 🏠 TRANG CHỦ: Hiển thị sản phẩm nổi bật
│       ├── chi_tiet_san_pham.html   ← 🔍 CHI TIẾT SẢN PHẨM: Gallery 4 ảnh, thêm giỏ
│       ├── gio_hang.html            ← 🛒 GIỎ HÀNG: Xem và chỉnh sửa giỏ hàng
│       ├── thanh_toan.html          ← 💳 THANH TOÁN: Form địa chỉ, chọn ship, chọn TT
│       ├── dat_hang_thanh_cong.html ← ✅ ĐẶT HÀNG THÀNH CÔNG: Timeline, VietQR, hóa đơn
│       ├── dang_nhap.html           ← 🔐 ĐĂNG NHẬP: Form đăng nhập (1-click với demo)
│       ├── dang_ky.html             ← 📝 ĐĂNG KÝ: Chọn vai trò Người Mua / Người Bán
│       ├── ho_so_ca_nhan.html       ← 👤 HỒ SƠ CÁ NHÂN: Xem và cập nhật thông tin
│       ├── lich_su_don_hang.html    ← 📋 LỊCH SỬ ĐƠN HÀNG: Danh sách đơn đã đặt
│       │
│       ├── nguoi_ban/               ← 🏪 KÊNH NGƯỜI BÁN
│       │   ├── tong_quan.html       ← Dashboard người bán (doanh thu, đơn hàng)
│       │   ├── danh_sach_san_pham.html ← Danh sách mô hình đang bán
│       │   ├── bieu_mau_san_pham.html  ← Form thêm/sửa mô hình (4 ảnh + preview)
│       │   └── danh_sach_don_hang.html ← Đơn hàng cần xử lý
│       │
│       └── quan_tri/                ← 👑 CỔNG QUẢN TRỊ ADMIN
│           ├── tong_quan.html       ← Dashboard admin (thống kê hệ thống)
│           ├── don_hang.html        ← Quản lý toàn bộ đơn hàng
│           ├── san_pham.html        ← Quản lý sản phẩm (toggle featured/stock)
│           ├── nguoi_dung.html      ← Quản lý tài khoản người dùng
│           └── danh_muc.html        ← Quản lý danh mục sản phẩm
│
├── tai_nguyen/                      ← 🎨 TÀI NGUYÊN TĨNH (Static Files)
│   ├── css/
│   │   └── style.css               ← CSS chính (luxury dark theme One Piece)
│   ├── js/                         ← JavaScript tùy chỉnh
│   └── hinh_anh/                   ← Hình ảnh
│       └── san_pham/               ← Ảnh mô hình (ace_fire.jpg, zoro_enma.jpg...)
│
├── db.sqlite3                       ← 💾 DATABASE SQLite (dữ liệu thật)
├── manage.py                        ← Lệnh quản lý Django (runserver, migrate...)
├── seed_data.py                     ← Script tạo dữ liệu mẫu (14 mô hình + 3 tài khoản)
├── requirements.txt                 ← Danh sách thư viện Python cần cài
└── venv/                            ← Môi trường Python ảo (không commit lên git)
```

---

## 🔑 FILE QUAN TRỌNG NHẤT — ĐỌC TRƯỚC

| File | Chức năng | Khi nào cần sửa |
|------|-----------|-----------------|
| `cua_hang/co_so_du_lieu.py` | Cấu trúc bảng database | Thêm/sửa trường dữ liệu → sau đó chạy `makemigrations` |
| `cua_hang/xu_ly_khach_hang.py` | Logic trang chủ, giỏ hàng, thanh toán | Sửa tính năng mua hàng |
| `cua_hang/xu_ly_tai_khoan.py` | Đăng nhập, đăng ký | Sửa quy trình tạo tài khoản |
| `cua_hang/xu_ly_nguoi_ban.py` | Logic kênh người bán | Sửa tính năng quản lý shop |
| `cua_hang/xu_ly_quan_tri.py` | Logic cổng admin | Sửa tính năng quản trị |
| `cua_hang/duong_dan_url.py` | URL patterns | Thêm trang mới |
| `du_an/settings.py` | Cài đặt toàn bộ | Đổi database, secret key, debug... |
| `tai_nguyen/css/style.css` | Toàn bộ giao diện | Sửa màu sắc, font, layout |

---

## 🚀 LỆNH THƯỜNG DÙNG

```powershell
# ▶️ Chạy website
.\venv\Scripts\python.exe manage.py runserver

# 🗄️ Tạo migration sau khi sửa co_so_du_lieu.py
.\venv\Scripts\python.exe manage.py makemigrations
.\venv\Scripts\python.exe manage.py migrate

# 🌱 Tạo lại dữ liệu mẫu
.\venv\Scripts\python.exe seed_data.py

# ✅ Kiểm tra lỗi
.\venv\Scripts\python.exe manage.py check

# 👑 Tạo tài khoản admin mới
.\venv\Scripts\python.exe manage.py createsuperuser
```

---

## 👥 TÀI KHOẢN DEMO

| Vai trò | Tên đăng nhập | Mật khẩu | Truy cập |
|---------|--------------|----------|----------|
| 🛒 Người Mua | `nguoimua` | `buyer123` | Mua hàng, xem đơn |
| 🏪 Người Bán | `nguoiban` | `seller123` | Kênh người bán |
| 👑 Admin | `admin` | `admin123` | Cổng quản trị |

---

## ⚠️ LƯU Ý QUAN TRỌNG

> **KHÔNG** đổi `label = 'shops'` trong `cua_hang/apps.py`  
> SQLite đang dùng tên bảng `shops_product`, `shops_order`... nếu đổi sẽ lỗi database!

> **KHÔNG** đổi `app_name = 'shops'` trong `cua_hang/duong_dan_url.py`  
> Tất cả template đang dùng `{% url 'shops:...' %}` — đổi sẽ lỗi toàn bộ link!

---

## 🎨 MÃ GIẢM GIÁ (để test thanh toán)

| Mã | Ưu đãi |
|----|--------|
| `LUFFY50K` | Giảm 50.000₫ |
| `ONEPIECE10` | Giảm 10% |
| `GEAR5` | Giảm 15% |
| `NAKAMA20` | Giảm 20% |
| `FREESHIP` | Miễn phí ship |

---

## 🌐 ĐỊA CHỈ TRANG WEB (URL)

Sau khi chạy server (`runserver`), truy cập tại `http://127.0.0.1:8000`

| Địa chỉ | Trang |
|---------|-------|
| `/` | 🏠 Trang chủ |
| `/san-pham/ten-mo-hinh/` | 🔍 Chi tiết sản phẩm |
| `/gio-hang/` | 🛒 Giỏ hàng |
| `/thanh-toan/` | 💳 Thanh toán |
| `/dang-nhap/` | 🔐 Đăng nhập |
| `/dang-ky/` | 📝 Đăng ký |
| `/ho-so/` | 👤 Hồ sơ cá nhân |
| `/kenh-nguoi-ban/` | 🏪 Dashboard người bán |
| `/kenh-nguoi-ban/san-pham/` | 📦 Danh sách sản phẩm shop |
| `/kenh-nguoi-ban/san-pham/them/` | ➕ Đăng sản phẩm mới |
| `/kenh-nguoi-ban/don-hang/` | 📋 Đơn hàng cần xử lý |
| `/quan-tri/` | 👑 Cổng quản trị admin |
| `/quan-tri/san-pham/` | Admin quản lý sản phẩm |
| `/quan-tri/nguoi-dung/` | Admin quản lý tài khoản |
| `/quan-tri/don-hang/` | Admin quản lý đơn hàng |
| `/quan-tri/danh-muc/` | Admin quản lý danh mục |
| `/admin/` | 🛠️ Django Admin (quản trị hệ thống) |
