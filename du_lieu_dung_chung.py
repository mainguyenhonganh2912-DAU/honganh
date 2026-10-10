# ==============================================================================
# 🌐 DỮ LIỆU DÙNG CHUNG TOÀN HỆ THỐNG (du_lieu_dung_chung.py)
# Context Processor tự động truyền các biến quan trọng tới TẤT CẢ các trang HTML:
# - all_categories: Toàn bộ danh mục mô hình One Piece để hiển thị menu
# - cart_total_items: Tổng số lượng mô hình đang có trong giỏ hàng (hiển thị trên icon giỏ)
# - user_role: Vai trò người dùng (guest, buyer, seller, admin)
# - is_buyer, is_seller, is_admin: Biến cờ tiện lợi cho điều kiện {% if %}
# - user_profile: Hồ sơ của tài khoản đang đăng nhập
# ==============================================================================

from .models import Category


def shop_context(request):
    """Truyền dữ liệu chung vào mọi template HTML"""
    categories = Category.objects.all()
    cart = request.session.get('cart', {})
    total_items = sum(cart.values())

    user_role = 'guest'
    is_buyer = False
    is_seller = False
    is_admin = False
    user_profile = None

    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            user_role = 'admin'
            is_admin = True
        elif hasattr(request.user, 'profile'):
            user_role = request.user.profile.role
            user_profile = request.user.profile
            if user_role == 'admin':
                is_admin = True
            elif user_role == 'seller':
                is_seller = True
            else:
                is_buyer = True
        else:
            user_role = 'buyer'
            is_buyer = True

    return {
        'all_categories': categories,
        'cart_total_items': total_items,
        'user_role': user_role,
        'is_buyer': is_buyer,
        'is_seller': is_seller,
        'is_admin': is_admin,
        'user_profile': user_profile,
    }
