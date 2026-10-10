# ==============================================================================
# 🧭 MIỀN ĐỊNH TUYẾN URL & ĐIỀU PHỐI / ROUTING & URL DISPATCHER DOMAIN
# File: cua_hang/duong_dan_url.py (và cua_hang/urls.py)
# Khai báo liên kết giữa các địa chỉ web URL và 4 miền xử lý trong views:
#   - Miền Khách hàng: Trang chủ, chi tiết mô hình, giỏ hàng, đặt hàng VietQR...
#   - Miền Tài khoản: Đăng nhập phân quyền, đăng ký, đăng xuất, hồ sơ...
#   - Miền Người bán: Tổng quan shop, thêm/sửa mô hình shop, đơn hàng shop...
#   - Miền Quản trị: Trung tâm quản trị sàn, duyệt đơn, thành viên, danh mục...
# ==============================================================================

from django.urls import path
from . import views

app_name = 'shops'

urlpatterns = [
    # 🛒 KHÁCH HÀNG: XEM SẢN PHẨM & MUA HÀNG
    path('', views.home, name='home'),
    path('san-pham/<slug:slug>/', views.product_detail, name='product_detail'),
    path('gio-hang/', views.cart_view, name='cart'),
    path('gio-hang/them/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('gio-hang/cap-nhat/', views.update_cart, name='update_cart'),
    path('gio-hang/xoa/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('gio-hang/xoa-tat-ca/', views.clear_cart, name='clear_cart'),
    path('gio-hang/ma-giam-gia/', views.apply_coupon, name='apply_coupon'),
    path('gio-hang/bo-ma-giam-gia/', views.remove_coupon, name='remove_coupon'),
    path('thanh-toan/', views.checkout, name='checkout'),
    path('dat-hang-thanh-cong/<str:order_code>/', views.order_success, name='order_success'),

    # 👤 TÀI KHOẢN & XÁC THỰC
    path('dang-nhap/', views.customer_login, name='login'),
    path('dang-ky/', views.customer_register, name='register'),
    path('dang-xuat/', views.customer_logout, name='logout'),
    path('ho-so/', views.customer_profile, name='profile'),

    # 🏪 KÊNH NGƯỜI BÁN (SELLER PORTAL)
    path('kenh-nguoi-ban/', views.seller_dashboard, name='seller_dashboard'),
    path('kenh-nguoi-ban/san-pham/', views.seller_products, name='seller_products'),
    path('kenh-nguoi-ban/san-pham/them/', views.seller_product_add, name='seller_product_add'),
    path('kenh-nguoi-ban/san-pham/<int:product_id>/sua/', views.seller_product_edit, name='seller_product_edit'),
    path('kenh-nguoi-ban/san-pham/<int:product_id>/xoa/', views.seller_product_delete, name='seller_product_delete'),
    path('kenh-nguoi-ban/don-hang/', views.seller_orders, name='seller_orders'),
    path('kenh-nguoi-ban/don-hang/<int:order_id>/trang-thai/', views.seller_order_status_update, name='seller_order_status_update'),

    # 👑 TRUNG TÂM QUẢN TRỊ WEB TRÊN FRONTEND (ADMIN PORTAL)
    path('quan-tri/', views.admin_portal_dashboard, name='admin_portal_dashboard'),
    path('quan-tri/don-hang/', views.admin_portal_orders, name='admin_portal_orders'),
    path('quan-tri/don-hang/<int:order_id>/trang-thai/', views.admin_portal_order_status, name='admin_portal_order_status'),
    path('quan-tri/san-pham/', views.admin_portal_products, name='admin_portal_products'),
    path('quan-tri/san-pham/<int:product_id>/noi-bat/', views.admin_portal_product_toggle_featured, name='admin_portal_product_toggle_featured'),
    path('quan-tri/san-pham/<int:product_id>/con-hang/', views.admin_portal_product_toggle_stock, name='admin_portal_product_toggle_stock'),
    path('quan-tri/san-pham/<int:product_id>/xoa/', views.admin_portal_product_delete, name='admin_portal_product_delete'),
    path('quan-tri/nguoi-dung/', views.admin_portal_users, name='admin_portal_users'),
    path('quan-tri/nguoi-dung/<int:user_id>/vai-tro/', views.admin_portal_user_change_role, name='admin_portal_user_change_role'),
    path('quan-tri/danh-muc/', views.admin_portal_categories, name='admin_portal_categories'),
    path('quan-tri/danh-muc/<int:category_id>/xoa/', views.admin_portal_category_delete, name='admin_portal_category_delete'),
]
