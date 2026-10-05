# One Piece Store — Django E-Commerce

> A full-featured e-commerce website for One Piece figure collectibles, built with **Python / Django**.  
> Supports 3 user roles: **Buyer** (customer), **Seller** (shop owner), and **Admin** (site administrator).

---

## System Architecture

```mermaid
flowchart TD
    subgraph CLIENT["🌐 Client (Browser)"]
        USER["👤 User / Browser"]
    end

    subgraph DJANGO["🐍 Django Application"]
        direction TB
        MAIN_URL["du_an/urls.py\n(Main Router)"]

        subgraph VIEWS["cua_hang/ — Business Logic"]
            V1["xu_ly_khach_hang.py\n(Customer Views)\nhome · cart · checkout · order"]
            V2["xu_ly_tai_khoan.py\n(Account Views)\nlogin · register · logout · profile"]
            V3["xu_ly_nguoi_ban.py\n(Seller Portal)\ndashboard · products · orders"]
            V4["xu_ly_quan_tri.py\n(Admin Portal)\nusers · products · categories · orders"]
        end

        subgraph MODELS["cua_hang/ — Database Models (co_so_du_lieu.py)"]
            M1["UserProfile\n(role: buyer / seller / admin)"]
            M2["Category\n(name · slug · icon)"]
            M3["Product\n(name · price · images · stock)"]
            M4["Order\n(COD / VietQR / MoMo)"]
            M5["OrderItem\n(product · quantity · price)"]
        end

        subgraph TEMPLATES["giao_dien/ — HTML Templates"]
            T1["base.html\n(Layout: Header + Footer)"]
            T2["cua_hang/\n(trang_chu · chi_tiet · gio_hang\ndang_nhap · dang_ky · thanh_toan)"]
            T3["cua_hang/nguoi_ban/\n(bieu_mau_san_pham · danh_sach_don_hang)"]
            T4["cua_hang/quan_tri/\n(Admin Portal pages)"]
        end

        URL_SHOP["cua_hang/duong_dan_url.py\n(Shop URL Patterns)"]
        ADMIN_PANEL["Django Admin Panel\n(/admin/)"]
    end

    subgraph DB["🗄️ Database"]
        SQLITE["db.sqlite3\n(SQLite)"]
    end

    subgraph STATIC["📦 Static & Media Files"]
        SF["staticfiles/\n(CSS · JS · Icons)"]
        TR["tai_nguyen/\n(Product Images)"]
    end

    subgraph SEED["🌱 Data Scripts"]
        SD["seed_data.py\n(Seed sample data)"]
        AD["du_an/add_data.py\n(Additional data loader)"]
    end

    subgraph DEPLOY["🚀 Deployment"]
        DF["Dockerfile"]
        RY["render.yaml"]
        PF["Procfile"]
        REQ["requirements.txt"]
    end

    USER -->|HTTP Request| MAIN_URL
    MAIN_URL -->|"path('')"| URL_SHOP
    MAIN_URL -->|"path('admin/')"| ADMIN_PANEL
    URL_SHOP --> V1
    URL_SHOP --> V2
    URL_SHOP --> V3
    URL_SHOP --> V4
    V1 & V2 & V3 & V4 -->|Query / Save| MODELS
    MODELS -->|Read / Write| SQLITE
    V1 & V2 & V3 & V4 -->|Render| TEMPLATES
    T2 & T3 & T4 -->|extends| T1
    TEMPLATES -->|HTML Response| USER
    SD & AD -->|"python manage.py / python seed_data.py"| SQLITE
    DF & RY & PF --> DJANGO
```

---

## Data Flow (Request → Response)

```mermaid
sequenceDiagram
    participant B as Browser
    participant R as du_an/urls.py (Router)
    participant V as cua_hang/views.py
    participant M as Models (co_so_du_lieu.py)
    participant DB as db.sqlite3
    participant T as giao_dien/ (Templates)

    B->>R: HTTP GET /
    R->>V: route to home() in xu_ly_khach_hang.py
    V->>M: Product.objects.filter(is_featured=True)
    M->>DB: SELECT * FROM product WHERE is_featured=1
    DB-->>M: Product rows
    M-->>V: QuerySet
    V->>T: render(request, "trang_chu.html", context)
    T-->>B: Full HTML page
```

---

## Database Schema (ER Diagram)

```mermaid
erDiagram
    User {
        int id PK
        string username
        string email
        string password
        bool is_staff
        bool is_superuser
    }
    UserProfile {
        int id PK
        int user_id FK
        string role
        string phone
        string shop_name
        string avatar
        text bio
    }
    Category {
        int id PK
        string name
        string slug
        string icon
    }
    Product {
        int id PK
        int category_id FK
        int seller_id FK
        string name
        string slug
        int price
        int original_price
        string height
        string scale
        string material
        string brand
        string weight
        text description
        string image
        string image_2
        string image_3
        string image_4
        bool is_featured
        bool in_stock
        datetime created_at
    }
    Order {
        int id PK
        int user_id FK
        string order_code
        string full_name
        string phone
        string email
        text address
        text note
        string payment_method
        string shipping_method
        string coupon_code
        int discount_amount
        int shipping_fee
        int total_price
        string status
        datetime created_at
    }
    OrderItem {
        int id PK
        int order_id FK
        int product_id FK
        string product_name
        int price
        int quantity
    }

    User ||--|| UserProfile : "has profile"
    User ||--o{ Order : "places"
    User ||--o{ Product : "sells"
    Category ||--o{ Product : "contains"
    Order ||--o{ OrderItem : "contains"
    Product ||--o{ OrderItem : "included in"
```

---

## User Roles & Permissions

```mermaid
flowchart LR
    subgraph ROLES["👥 User Roles"]
        BUYER["🛍️ Buyer\n(role: buyer)"]
        SELLER["🏪 Seller\n(role: seller)"]
        ADMIN["🛡️ Admin\n(role: admin)"]
    end

    subgraph BUYER_FEATURES["Buyer Features"]
        BF1["Browse products\n(trang_chu.html)"]
        BF2["View product detail\n(chi_tiet_san_pham.html)"]
        BF3["Shopping cart\n(gio_hang.html)"]
        BF4["Checkout\n(thanh_toan.html)"]
        BF5["Order history\n(ho_so_ca_nhan.html)"]
    end

    subgraph SELLER_FEATURES["Seller Portal"]
        SF1["Seller Dashboard"]
        SF2["Manage Products\n(Add / Edit / Delete)"]
        SF3["View & Update Orders"]
    end

    subgraph ADMIN_FEATURES["Admin Portal"]
        AF1["Admin Dashboard"]
        AF2["Manage All Users\n(change roles)"]
        AF3["Manage All Products\n(feature / stock / delete)"]
        AF4["Manage All Orders\n(update status)"]
        AF5["Manage Categories"]
        AF6["Django Admin Panel\n(/admin/)"]
    end

    BUYER --> BUYER_FEATURES
    SELLER --> BUYER_FEATURES
    SELLER --> SELLER_FEATURES
    ADMIN --> BUYER_FEATURES
    ADMIN --> SELLER_FEATURES
    ADMIN --> ADMIN_FEATURES
```

---

## Project Structure

```
One-Piece-Store/
├── du_an/                        # Django project config
│   ├── settings.py               # Database, static files, security settings
│   ├── urls.py                   # Main URL router
│   ├── wsgi.py / asgi.py         # Web server interface
│   └── add_data.py               # Additional data loader script
│
├── cua_hang/                     # Main Django app — all business logic
│   ├── co_so_du_lieu.py          # ★ Database models (UserProfile, Category, Product, Order, OrderItem)
│   ├── models.py                 # Re-exports from co_so_du_lieu.py
│   ├── duong_dan_url.py          # ★ All URL patterns for the shop
│   ├── urls.py                   # Re-exports from duong_dan_url.py
│   ├── xu_ly_khach_hang.py       # Customer views (home, cart, checkout, orders)
│   ├── xu_ly_tai_khoan.py        # Account views (login, register, logout, profile)
│   ├── xu_ly_nguoi_ban.py        # Seller portal views
│   ├── xu_ly_quan_tri.py         # Admin portal views
│   ├── context_processors.py     # Global template context (cart count, etc.)
│   ├── du_lieu_dung_chung.py     # Shared data utilities
│   ├── admin.py                  # Django admin registration
│   └── migrations/               # Database migration files
│
├── giao_dien/                    # HTML Templates (Frontend)
│   ├── base.html                 # Base layout (Header + Footer)
│   ├── cua_hang/                 # Customer-facing pages
│   │   ├── trang_chu.html        # Homepage
│   │   ├── chi_tiet_san_pham.html# Product detail page
│   │   ├── gio_hang.html         # Shopping cart
│   │   ├── thanh_toan.html       # Checkout
│   │   ├── dat_hang_thanh_cong.html # Order success
│   │   ├── dang_nhap.html        # Login page
│   │   ├── dang_ky.html          # Register page
│   │   ├── ho_so_ca_nhan.html    # User profile & order history
│   │   ├── nguoi_ban/            # Seller portal pages
│   │   └── quan_tri/             # Admin portal pages
│   └── admin/                   # Custom Django admin templates
│
├── staticfiles/                  # Collected static files (CSS, JS, icons)
├── tai_nguyen/                   # Media/resource files (product images)
├── seed_data.py                  # Script to seed sample data into DB
├── db.sqlite3                    # SQLite database file
├── manage.py                     # Django management CLI
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker container config
├── render.yaml                   # Render.com deployment config
└── Procfile                      # Process config for Heroku / Render
```

---

## Setup & Run Locally

```bash
# 1. Clone the repository
git clone <repo-url>
cd One-Piece-Store

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Seed sample data
python seed_data.py

# 6. Create superuser (Admin)
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
# Visit: http://127.0.0.1:8000
```

## Deployment

| File | Purpose |
|------|---------|
| `Dockerfile` | Containerize the app with Docker |
| `render.yaml` | One-click deploy to [Render.com](https://render.com) |
| `Procfile` | Process definition for Heroku / Render |
| `requirements.txt` | Python package list |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3 + Django 5 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | HTML5 + CSS3 + Bootstrap |
| Static Files | WhiteNoise |
| Deployment | Docker / Render.com |
| Payment | COD · VietQR Bank Transfer · MoMo |
