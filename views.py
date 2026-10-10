# ==============================================================================
# 🧠 TRUNG TÂM TỔNG HỢP 4 MIỀN NGHIỆP VỤ / 4-DOMAIN BUSINESS VIEWS DISPATCHER
# File: cua_hang/views.py
# Gom nhóm và tái xuất (re-export) đầy đủ 4 miền nghiệp vụ cân đối:
# 
# 1. MIỀN KHÁCH HÀNG (cua_hang/xu_ly_khach_hang.py):
#    - home, product_detail, cart_view, add_to_cart, update_cart,
#    - remove_from_cart, clear_cart, apply_coupon, remove_coupon,
#    - checkout, order_success
#
# 2. MIỀN TÀI KHOẢN & PHÂN QUYỀN (cua_hang/xu_ly_tai_khoan.py):
#    - customer_login, customer_register, customer_logout, customer_profile
#
# 3. MIỀN KÊNH NGƯỜI BÁN (cua_hang/xu_ly_nguoi_ban.py):
#    - seller_required, seller_dashboard, seller_products, seller_product_add,
#    - seller_product_edit, seller_product_delete, seller_orders, seller_order_status_update
#
# 4. MIỀN TRUNG TÂM QUẢN TRỊ (cua_hang/xu_ly_quan_tri.py):
#    - admin_portal_required, admin_portal_dashboard, admin_portal_orders,
#    - admin_portal_order_status, admin_portal_products, admin_portal_product_toggle_featured,
#    - admin_portal_product_toggle_stock, admin_portal_product_delete,
#    - admin_portal_users, admin_portal_user_change_role, admin_portal_categories,
#    - admin_portal_category_delete
# ==============================================================================

# 1. Các hàm xử lý giao diện mua sắm khách hàng
from .xu_ly_khach_hang import (
    home,
    product_detail,
    cart_view,
    add_to_cart,
    update_cart,
    remove_from_cart,
    clear_cart,
    apply_coupon,
    remove_coupon,
    checkout,
    order_success,
    COUPONS
)

# 2. Các hàm xử lý tài khoản, đăng nhập & đăng ký
from .xu_ly_tai_khoan import (
    customer_login,
    customer_register,
    customer_logout,
    customer_profile
)

# 3. Các hàm xử lý kênh người bán (Seller Portal)
from .xu_ly_nguoi_ban import (
    seller_required,
    seller_dashboard,
    seller_products,
    seller_product_add,
    seller_product_edit,
    seller_product_delete,
    seller_orders,
    seller_order_status_update
)

# 4. Các hàm xử lý trung tâm quản trị web (Admin Portal)
from .xu_ly_quan_tri import (
    admin_portal_required,
    admin_portal_dashboard,
    admin_portal_orders,
    admin_portal_order_status,
    admin_portal_products,
    admin_portal_product_toggle_featured,
    admin_portal_product_toggle_stock,
    admin_portal_product_delete,
    admin_portal_users,
    admin_portal_user_change_role,
    admin_portal_categories,
    admin_portal_category_delete
)
