# ==============================================================================
# 👑 MIỀN QUẢN TRỊ TOÀN SÀN / ADMIN & SYSTEM GOVERNANCE DOMAIN
# File: cua_hang/xu_ly_quan_tri.py
# Chứa toàn bộ các hàm điều hành hệ thống toàn sàn:
#   1. admin_portal_required: Bộ lọc chỉ cho phép Quản trị viên (Admin) truy cập
#   2. admin_portal_dashboard: Bảng điều khiển doanh số, biểu đồ tăng trưởng
#   3. admin_portal_orders: Quản lý và duyệt toàn bộ đơn hàng
#   4. admin_portal_order_status: Cập nhật trạng thái đơn hàng toàn sàn
#   5. admin_portal_products: Quản lý toàn bộ sản phẩm trên web
#   6. admin_portal_product_toggle_featured: Bật/tắt ghim sản phẩm HOT
#   7. admin_portal_product_toggle_stock: Bật/tắt trạng thái Còn/Hết hàng
#   8. admin_portal_product_delete: Xóa sản phẩm khỏi hệ thống
#   9. admin_portal_users: Quản lý thành viên & phân quyền (Buyer, Seller, Admin)
#   10. admin_portal_user_change_role: Thay đổi quyền của tài khoản
#   11. admin_portal_categories: Quản lý danh mục mô hình One Piece
#   12. admin_portal_category_delete: Xóa danh mục
# Liên kết CSDL: Toàn bộ bảng User, UserProfile, Category, Product, Order, OrderItem
# ==============================================================================

from functools import wraps
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Sum, Count
from django.utils import timezone
from django.utils.text import slugify
from .models import Category, Product, Order, OrderItem, UserProfile


def admin_portal_required(view_func):
    """Bảo vệ trang Trung Tâm Quản Trị Web: Chỉ cho phép tài khoản admin"""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Vui lòng đăng nhập với tư cách Quản Trị Viên!")
            return redirect('shops:login')
        role = getattr(getattr(request.user, 'profile', None), 'role', 'buyer')
        if not (request.user.is_superuser or request.user.is_staff or role == 'admin'):
            messages.error(request, "Chỉ Quản Trị Viên mới có quyền truy cập Trung Tâm Quản Trị Web!")
            return redirect('shops:home')
        return view_func(request, *args, **kwargs)
    return _wrapped


@admin_portal_required
def admin_portal_dashboard(request):
    """Tổng quan doanh thu, số liệu tài chính toàn sàn"""
    total_revenue = Order.objects.exclude(status='cancelled').aggregate(total=Sum('total_price'))['total'] or 0
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    completed_orders = Order.objects.filter(status='completed').count()

    total_products = Product.objects.count()
    total_users = User.objects.count()
    total_sellers = UserProfile.objects.filter(role='seller').count()
    total_buyers = UserProfile.objects.filter(role='buyer').count()

    # Thống kê doanh thu 7 ngày qua
    today = timezone.now().date()
    daily_stats = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        rev = Order.objects.filter(created_at__date=d).exclude(status='cancelled').aggregate(total=Sum('total_price'))['total'] or 0
        daily_stats.append({
            'date': d.strftime('%d/%m'),
            'revenue': rev,
        })

    recent_orders = Order.objects.all().order_by('-created_at')[:8]
    recent_users = User.objects.all().order_by('-date_joined')[:6]

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_products': total_products,
        'total_users': total_users,
        'total_sellers': total_sellers,
        'total_buyers': total_buyers,
        'daily_stats': daily_stats,
        'recent_orders': recent_orders,
        'recent_users': recent_users,
    }
    return render(request, 'cua_hang/quan_tri/tong_quan.html', context)


@admin_portal_required
def admin_portal_orders(request):
    """Quản lý toàn bộ đơn hàng trên sàn"""
    orders = Order.objects.all().order_by('-created_at')

    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)

    q = request.GET.get('q', '').strip()
    if q:
        orders = orders.filter(
            Q(order_code__icontains=q) |
            Q(full_name__icontains=q) |
            Q(phone__icontains=q)
        )

    context = {
        'orders': orders,
        'current_status': status_filter,
        'search_query': q,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'cua_hang/quan_tri/quan_ly_don_hang.html', context)


@admin_portal_required
def admin_portal_order_status(request, order_id):
    """Admin cập nhật trạng thái đơn hàng"""
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Đã cập nhật đơn hàng #{order.order_code} thành: {order.get_status_display()}")

    next_url = request.POST.get('next', '').strip()
    if next_url and next_url.startswith('/'):
        return redirect(next_url)
    return redirect('shops:admin_portal_orders')


@admin_portal_required
def admin_portal_products(request):
    """Quản lý toàn bộ sản phẩm trên hệ thống"""
    products = Product.objects.all()
    categories = Category.objects.all()

    q = request.GET.get('q', '').strip()
    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(category__name__icontains=q) |
            Q(brand__icontains=q)
        )

    cat_slug = request.GET.get('category')
    if cat_slug:
        products = products.filter(category__slug=cat_slug)

    context = {
        'products': products,
        'categories': categories,
        'total_count': products.count(),
        'search_query': q,
        'selected_category': cat_slug,
    }
    return render(request, 'cua_hang/quan_tri/quan_ly_san_pham.html', context)


@admin_portal_required
def admin_portal_product_toggle_featured(request, product_id):
    """Bật/tắt ghim sản phẩm HOT trang chủ"""
    product = get_object_or_404(Product, id=product_id)
    product.is_featured = not product.is_featured
    product.save()
    status_text = "Nổi bật (HOT)" if product.is_featured else "Bình thường"
    messages.success(request, f"Đã chuyển mô hình '{product.name}' sang: {status_text}")
    referer = request.META.get('HTTP_REFERER', '')
    if referer and referer.startswith('http'):
        return redirect(referer)
    return redirect('shops:admin_portal_products')


@admin_portal_required
def admin_portal_product_toggle_stock(request, product_id):
    """Bật/tắt trạng thái Còn hàng"""
    product = get_object_or_404(Product, id=product_id)
    product.in_stock = not product.in_stock
    product.save()
    status_text = "Còn Hàng" if product.in_stock else "Hết Hàng"
    messages.success(request, f"Đã cập nhật tình trạng mô hình '{product.name}': {status_text}")
    referer = request.META.get('HTTP_REFERER', '')
    if referer and referer.startswith('http'):
        return redirect(referer)
    return redirect('shops:admin_portal_products')


@admin_portal_required
def admin_portal_product_delete(request, product_id):
    """Admin xóa sản phẩm vi phạm"""
    product = get_object_or_404(Product, id=product_id)
    name = product.name
    product.delete()
    messages.info(request, f"Đã xóa vĩnh viễn mô hình '{name}'.")
    return redirect('shops:admin_portal_products')


@admin_portal_required
def admin_portal_users(request):
    """Quản lý thành viên & phân quyền (Buyer, Seller, Admin)"""
    users = User.objects.all().order_by('-date_joined')
    q = request.GET.get('q', '').strip()
    if q:
        users = users.filter(
            Q(username__icontains=q) |
            Q(first_name__icontains=q) |
            Q(email__icontains=q)
        )

    role_filter = request.GET.get('role')
    if role_filter:
        users = users.filter(profile__role=role_filter)

    context = {
        'users': users,
        'total_count': users.count(),
        'search_query': q,
        'current_role': role_filter,
    }
    return render(request, 'cua_hang/quan_tri/quan_ly_nguoi_dung.html', context)


@admin_portal_required
def admin_portal_user_change_role(request, user_id):
    """Admin thay đổi quyền của tài khoản"""
    if request.method == 'POST':
        target_user = get_object_or_404(User, id=user_id)
        new_role = request.POST.get('role')

        if new_role in ['buyer', 'seller', 'admin']:
            profile, _ = UserProfile.objects.get_or_create(user=target_user)
            profile.role = new_role
            if new_role == 'admin':
                target_user.is_staff = True
            elif new_role == 'seller':
                target_user.is_staff = False
                if not profile.shop_name:
                    profile.shop_name = f"Shop {target_user.first_name or target_user.username}"
            else:
                target_user.is_staff = False

            target_user.save()
            profile.save()
            messages.success(request, f"Đã cập nhật quyền của '{target_user.username}' thành: {profile.get_role_display()}")

    return redirect('shops:admin_portal_users')


@admin_portal_required
def admin_portal_categories(request):
    """Quản lý danh mục mô hình"""
    categories = Category.objects.annotate(product_count=Count('products')).all()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        icon = request.POST.get('icon', 'fa-skull').strip()

        if name:
            slug = slugify(name)
            if Category.objects.filter(slug=slug).exists():
                messages.error(request, f"Danh mục '{name}' đã tồn tại!")
            else:
                Category.objects.create(name=name, slug=slug, icon=icon)
                messages.success(request, f"Đã tạo mới danh mục '{name}' thành công!")
                return redirect('shops:admin_portal_categories')

    context = {
        'categories': categories,
    }
    return render(request, 'cua_hang/quan_tri/quan_ly_danh_muc.html', context)


@admin_portal_required
def admin_portal_category_delete(request, category_id):
    """Xóa danh mục"""
    category = get_object_or_404(Category, id=category_id)
    name = category.name
    category.delete()
    messages.info(request, f"Đã xóa danh mục '{name}'.")
    return redirect('shops:admin_portal_categories')
