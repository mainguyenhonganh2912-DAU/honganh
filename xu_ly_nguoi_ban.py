# ==============================================================================
# 🏪 MIỀN KÊNH NGƯỜI BÁN / SELLER & MERCHANT PORTAL DOMAIN
# File: cua_hang/xu_ly_nguoi_ban.py
# Chứa toàn bộ các hàm quản lý dành cho Chủ gian hàng / Shop:
#   1. seller_required: Bộ lọc bảo mật chỉ cho phép Người bán / Admin truy cập
#   2. seller_dashboard: Thống kê doanh thu, đơn hàng, mô hình của gian hàng
#   3. seller_products: Danh sách mô hình đang bán của shop
#   4. seller_product_add: Đăng bán mô hình mới (hỗ trợ nhập 4 góc ảnh chi tiết)
#   5. seller_product_edit: Chỉnh sửa thông tin, giá bán, ảnh mô hình
#   6. seller_product_delete: Xóa mô hình khỏi gian hàng
#   7. seller_orders: Quản lý các đơn hàng khách đặt mua từ shop
#   8. seller_order_status_update: Cập nhật trạng thái đơn (chờ duyệt, đang giao, hoàn thành)
# Liên kết CSDL: Product (seller=User), Order, Category (trong co_so_du_lieu.py)
# ==============================================================================

import uuid
from functools import wraps
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.utils.text import slugify
from .models import Category, Product, Order, OrderItem


def seller_required(view_func):
    """Bảo vệ trang Kênh Người Bán: Chỉ cho phép tài khoản có vai trò seller hoặc admin"""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Vui lòng đăng nhập để truy cập Kênh Người Bán!")
            return redirect('shops:login')
        role = getattr(getattr(request.user, 'profile', None), 'role', 'buyer')
        if not (request.user.is_superuser or request.user.is_staff or role in ['seller', 'admin']):
            messages.error(request, "Tài khoản của bạn là Người Mua. Bạn hãy đăng ký mở Gian Hàng để vào Kênh Người Bán!")
            return redirect('shops:home')
        return view_func(request, *args, **kwargs)
    return _wrapped


@seller_required
def seller_dashboard(request):
    """Bảng điều khiển kinh doanh của Người Bán"""
    my_products = Product.objects.filter(seller=request.user)
    total_products = my_products.count()
    in_stock_products = my_products.filter(in_stock=True).count()
    out_of_stock_products = total_products - in_stock_products

    # Lấy các mục đơn hàng chứa sản phẩm của người bán này
    seller_items = OrderItem.objects.filter(product__seller=request.user).select_related('order', 'product')
    seller_revenue = sum(item.price * item.quantity for item in seller_items.exclude(order__status='cancelled'))

    # Danh sách các đơn hàng chứa sản phẩm của shop
    orders_qs = Order.objects.filter(items__product__seller=request.user).distinct().order_by('-created_at')
    total_orders = orders_qs.count()
    pending_orders = orders_qs.filter(status='pending').count()
    completed_orders = orders_qs.filter(status='completed').count()

    recent_orders = orders_qs[:6]
    recent_products = my_products.order_by('-created_at')[:5]

    context = {
        'total_products': total_products,
        'in_stock_products': in_stock_products,
        'out_of_stock_products': out_of_stock_products,
        'seller_revenue': seller_revenue,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'recent_orders': recent_orders,
        'recent_products': recent_products,
        'shop_name': getattr(getattr(request.user, 'profile', None), 'shop_name', 'Gian Hàng Của Tôi'),
    }
    return render(request, 'cua_hang/nguoi_ban/tong_quan.html', context)


@seller_required
def seller_products(request):
    """Quản lý danh sách mô hình của Người Bán"""
    products = Product.objects.filter(seller=request.user)
    categories = Category.objects.all()

    q = request.GET.get('q', '').strip()
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))

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
    return render(request, 'cua_hang/nguoi_ban/danh_sach_san_pham.html', context)


@seller_required
def seller_product_add(request):
    """Đăng bán mô hình mới với ảnh chính và ảnh chi tiết"""
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category_id = request.POST.get('category_id')
        price = request.POST.get('price', 0)
        original_price = request.POST.get('original_price', '').strip()
        height = request.POST.get('height', '20 cm').strip()
        scale = request.POST.get('scale', 'Tỷ lệ 1/7').strip()
        material = request.POST.get('material', 'PVC cao cấp').strip()
        brand = request.POST.get('brand', 'Bandai / Banpresto').strip()
        weight = request.POST.get('weight', '850g').strip()
        
        # 4 góc ảnh chi tiết
        image = request.POST.get('image', '').strip() or 'https://via.placeholder.com/600x600'
        image_2 = request.POST.get('image_2', '').strip()
        image_3 = request.POST.get('image_3', '').strip()
        image_4 = request.POST.get('image_4', '').strip()
        
        description = request.POST.get('description', '').strip()
        in_stock = request.POST.get('in_stock') == 'on'

        if not name or not category_id or not price:
            messages.error(request, "Vui lòng nhập đầy đủ Tên mô hình, Danh mục và Giá bán!")
            return render(request, 'cua_hang/nguoi_ban/bieu_mau_san_pham.html', {'categories': categories, 'is_edit': False})

        # Tạo slug độc nhất
        base_slug = slugify(name)
        if not base_slug:
            base_slug = f"mo-hinh-{uuid.uuid4().hex[:6]}"
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        category = get_object_or_404(Category, id=category_id)
        product = Product.objects.create(
            seller=request.user,
            category=category,
            name=name,
            slug=slug,
            price=int(price),
            original_price=int(original_price) if original_price else None,
            height=height,
            scale=scale,
            material=material,
            brand=brand,
            weight=weight,
            image=image,
            image_2=image_2 if image_2 else None,
            image_3=image_3 if image_3 else None,
            image_4=image_4 if image_4 else None,
            description=description,
            in_stock=in_stock,
        )
        messages.success(request, f"Đã đăng bán thành công mô hình '{product.name}'!")
        return redirect('shops:seller_products')

    return render(request, 'cua_hang/nguoi_ban/bieu_mau_san_pham.html', {'categories': categories, 'is_edit': False})


@seller_required
def seller_product_edit(request, product_id):
    """Chỉnh sửa thông tin mô hình"""
    if request.user.is_superuser or request.user.is_staff:
        product = get_object_or_404(Product, id=product_id)
    else:
        product = get_object_or_404(Product, id=product_id, seller=request.user)

    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category_id = request.POST.get('category_id')
        price = request.POST.get('price', 0)
        original_price = request.POST.get('original_price', '').strip()

        if not name or not category_id or not price:
            messages.error(request, "Vui lòng điền đủ các thông tin bắt buộc!")
            return render(request, 'cua_hang/nguoi_ban/bieu_mau_san_pham.html', {'product': product, 'categories': categories, 'is_edit': True})

        product.name = name
        product.category = get_object_or_404(Category, id=category_id)
        product.price = int(price)
        product.original_price = int(original_price) if original_price else None
        product.height = request.POST.get('height', '20 cm').strip()
        product.scale = request.POST.get('scale', 'Tỷ lệ 1/7').strip()
        product.material = request.POST.get('material', 'PVC cao cấp').strip()
        product.brand = request.POST.get('brand', 'Bandai / Banpresto').strip()
        product.weight = request.POST.get('weight', '850g').strip()
        
        product.image = request.POST.get('image', '').strip() or product.image
        product.image_2 = request.POST.get('image_2', '').strip() or None
        product.image_3 = request.POST.get('image_3', '').strip() or None
        product.image_4 = request.POST.get('image_4', '').strip() or None
        
        product.description = request.POST.get('description', '').strip()
        product.in_stock = request.POST.get('in_stock') == 'on'
        product.save()

        messages.success(request, f"Đã cập nhật mô hình '{product.name}' thành công!")
        return redirect('shops:seller_products')

    return render(request, 'cua_hang/nguoi_ban/bieu_mau_san_pham.html', {'product': product, 'categories': categories, 'is_edit': True})


@seller_required
def seller_product_delete(request, product_id):
    """Xóa mô hình khỏi gian hàng"""
    if request.user.is_superuser or request.user.is_staff:
        product = get_object_or_404(Product, id=product_id)
    else:
        product = get_object_or_404(Product, id=product_id, seller=request.user)

    name = product.name
    product.delete()
    messages.info(request, f"Đã xóa mô hình '{name}' khỏi gian hàng.")
    return redirect('shops:seller_products')


@seller_required
def seller_orders(request):
    """Quản lý các đơn hàng chứa sản phẩm của Người Bán"""
    orders = Order.objects.filter(items__product__seller=request.user).distinct().order_by('-created_at')

    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)

    context = {
        'orders': orders,
        'current_status': status_filter,
    }
    return render(request, 'cua_hang/nguoi_ban/danh_sach_don_hang.html', context)


@seller_required
def seller_order_status_update(request, order_id):
    """Người bán cập nhật trạng thái đơn hàng"""
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        # Kiểm tra xem đơn này có sản phẩm của người bán không
        if not request.user.is_superuser and not order.items.filter(product__seller=request.user).exists():
            messages.error(request, "Bạn không có quyền chỉnh sửa đơn hàng này!")
            return redirect('shops:seller_orders')

        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Đã cập nhật trạng thái đơn #{order.order_code} thành: {order.get_status_display()}")

    next_url = request.POST.get('next', '').strip()
    if next_url and next_url.startswith('/'):
        return redirect(next_url)
    return redirect('shops:seller_orders')
