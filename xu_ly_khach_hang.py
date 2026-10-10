# ==============================================================================
# 🛒 MIỀN NGHIỆP VỤ KHÁCH HÀNG / CUSTOMER & SHOPPING DOMAIN
# File: cua_hang/xu_ly_khach_hang.py
# Chứa toàn bộ các hàm phục vụ trải nghiệm mua sắm của khách:
#   1. home: Trang chủ (tìm kiếm, lọc theo danh mục, lọc theo khoảng giá, sắp xếp)
#   2. product_detail: Xem chi tiết mô hình, thư viện ảnh đa góc, mô hình liên quan
#   3. cart_view: Xem giỏ hàng, tính tổng tiền, thanh tiến độ freeship
#   4. add_to_cart: Thêm sản phẩm vào giỏ (hỗ trợ mua ngay)
#   5. update_cart: Tăng/giảm số lượng
#   6. remove_from_cart: Xóa sản phẩm khỏi giỏ
#   7. clear_cart: Xóa trắng giỏ hàng
#   8. apply_coupon / remove_coupon: Áp dụng hoặc hủy mã giảm giá (Voucher)
#   9. checkout: Điền thông tin giao hàng, chọn COD / Napas VietQR / MoMo
#   10. order_success: Đặt hàng thành công, hiển thị mã VietQR chuyển khoản tự động
# Liên kết CSDL: Category, Product, Order, OrderItem (trong co_so_du_lieu.py)
# ==============================================================================

import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .models import Category, Product, Order, OrderItem

# Danh sách mã giảm giá Nakama độc quyền
COUPONS = {
    'LUFFY50K': {'type': 'fixed', 'value': 50000, 'label': 'Voucher Giảm 50.000 VNĐ'},
    'ONEPIECE10': {'type': 'percent', 'value': 10, 'label': 'Voucher Giảm 10% Tổng Đơn'},
    'FREESHIP': {'type': 'freeship', 'value': 0, 'label': 'Miễn Phí Vận Chuyển Toàn Quốc'},
    'GEAR5': {'type': 'percent', 'value': 15, 'label': 'Voucher Thần Mặt Trời Nika Giảm 15%'},
    'NAKAMA20': {'type': 'percent', 'value': 20, 'label': 'Voucher Tri Ân Nakama Giảm 20%'},
}


def home(request):
    """Trang chủ hiển thị danh sách mô hình One Piece, bộ lọc và tìm kiếm"""
    products = Product.objects.all()
    categories = Category.objects.all()

    # Tìm kiếm theo tên, mô tả hoặc danh mục
    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    # Lọc theo Danh mục
    category_slug = request.GET.get('category', '')
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    # Lọc theo Khoảng giá
    price_range = request.GET.get('price', '')
    if price_range == 'under_500':
        products = products.filter(price__lt=500000)
    elif price_range == '500_1000':
        products = products.filter(price__gte=500000, price__lte=1000000)
    elif price_range == '1000_2000':
        products = products.filter(price__gte=1000000, price__lte=2000000)
    elif price_range == 'over_2000':
        products = products.filter(price__gt=2000000)

    # Sắp xếp
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'popular':
        products = products.order_by('-is_featured', '-created_at')
    else:
        products = products.order_by('-created_at')

    # Sản phẩm HOT / Nổi bật
    featured_products = Product.objects.filter(is_featured=True)[:8]

    # Phân trang (8 sản phẩm mỗi trang)
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'categories': categories,
        'current_category': current_category,
        'featured_products': featured_products,
        'query': query,
        'price_range': price_range,
        'sort_by': sort_by,
        'total_count': products.count(),
    }
    return render(request, 'cua_hang/trang_chu.html', context)


def product_detail(request, slug):
    """Trang xem chi tiết mô hình, thông số và thư viện ảnh đa góc"""
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'cua_hang/chi_tiet_san_pham.html', context)


def cart_view(request):
    """Trang xem giỏ hàng và áp mã giảm giá"""
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    cart_product_ids = []

    for product_id, qty in cart.items():
        try:
            prod = Product.objects.get(id=int(product_id))
            subtotal = prod.price * qty
            total_price += subtotal
            cart_items.append({
                'product': prod,
                'quantity': qty,
                'subtotal': subtotal,
            })
            cart_product_ids.append(prod.id)
        except (Product.DoesNotExist, ValueError):
            continue

    # Xử lý Mã Giảm Giá
    coupon_code = request.session.get('coupon_code')
    coupon_info = COUPONS.get(coupon_code) if coupon_code else None
    discount_amount = 0

    if coupon_info:
        if coupon_info['type'] == 'fixed':
            discount_amount = min(coupon_info['value'], total_price)
        elif coupon_info['type'] == 'percent':
            discount_amount = int(total_price * (coupon_info['value'] / 100))

    # Miễn phí vận chuyển nếu đơn hàng từ 500.000 VNĐ hoặc có mã FREESHIP
    freeship_threshold = 500000
    has_freeship_coupon = (coupon_info and coupon_info['type'] == 'freeship')

    if total_price == 0:
        shipping_fee = 0
    elif total_price >= freeship_threshold or has_freeship_coupon:
        shipping_fee = 0
    else:
        shipping_fee = 30000

    freeship_gap = max(0, freeship_threshold - total_price)
    freeship_percent = min(100, int((total_price / freeship_threshold) * 100)) if total_price > 0 else 0
    final_total = max(0, total_price - discount_amount + shipping_fee)

    # Gợi ý mô hình HOT khác chưa có trong giỏ
    suggested_products = Product.objects.filter(in_stock=True).exclude(id__in=cart_product_ids).order_by('-is_featured', '-created_at')[:4]

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'discount_amount': discount_amount,
        'coupon_code': coupon_code,
        'coupon_info': coupon_info,
        'shipping_fee': shipping_fee,
        'freeship_threshold': freeship_threshold,
        'freeship_gap': freeship_gap,
        'freeship_percent': freeship_percent,
        'final_total': final_total,
        'suggested_products': suggested_products,
        'coupons_list': COUPONS,
    }
    return render(request, 'cua_hang/gio_hang.html', context)


def apply_coupon(request):
    """Áp dụng mã giảm giá vào đơn hàng"""
    if request.method == 'POST':
        code = request.POST.get('coupon_code', '').strip().upper()
        if code in COUPONS:
            request.session['coupon_code'] = code
            request.session.modified = True
            messages.success(request, f"Đã áp dụng mã {code}: {COUPONS[code]['label']}!")
        else:
            messages.error(request, f"Mã giảm giá '{code}' không tồn tại hoặc đã hết hạn!")

    referer = request.META.get('HTTP_REFERER', '')
    if referer and referer.startswith('http'):
        return redirect(referer)
    return redirect('shops:cart')


def remove_coupon(request):
    """Hủy mã giảm giá đã áp dụng"""
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
        request.session.modified = True
        messages.info(request, 'Đã gỡ bỏ mã giảm giá.')
    referer = request.META.get('HTTP_REFERER', '')
    if referer and referer.startswith('http'):
        return redirect(referer)
    return redirect('shops:cart')


def clear_cart(request):
    """Xóa toàn bộ sản phẩm trong giỏ hàng"""
    request.session['cart'] = {}
    request.session.pop('coupon_code', None)
    request.session.modified = True
    messages.info(request, "Đã làm trống giỏ hàng của bạn.")
    return redirect('shops:cart')


def add_to_cart(request, product_id):
    """Thêm sản phẩm vào giỏ hàng"""
    product = get_object_or_404(Product, id=product_id)
    try:
        qty = int(request.POST.get('quantity', 1))
        if qty < 1:
            qty = 1
    except ValueError:
        qty = 1

    cart = request.session.get('cart', {})
    prod_id_str = str(product_id)
    cart[prod_id_str] = cart.get(prod_id_str, 0) + qty
    request.session['cart'] = cart
    request.session.modified = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': f"Đã thêm '{product.name}' vào giỏ hàng!",
            'total_items': sum(cart.values())
        })

    messages.success(request, f"Đã thêm '{product.name}' vào giỏ hàng thành công!")
    if request.POST.get('buy_now') == '1':
        return redirect('shops:checkout')
    referer = request.POST.get('next', '').strip() or request.META.get('HTTP_REFERER', '')
    if referer and (referer.startswith('/') or referer.startswith('http')):
        return redirect(referer)
    return redirect('shops:cart')


def update_cart(request):
    """Cập nhật số lượng mô hình trong giỏ"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        cart = request.session.get('cart', {})

        if product_id in cart:
            if action == 'increase':
                cart[product_id] += 1
            elif action == 'decrease':
                cart[product_id] -= 1
                if cart[product_id] <= 0:
                    del cart[product_id]
            elif action == 'remove':
                del cart[product_id]
            elif action == 'set':
                try:
                    qty = int(request.POST.get('quantity', 1))
                    if qty > 0:
                        cart[product_id] = qty
                    else:
                        del cart[product_id]
                except ValueError:
                    pass

            request.session['cart'] = cart
            request.session.modified = True

    return redirect('shops:cart')


def remove_from_cart(request, product_id):
    """Xóa 1 sản phẩm khỏi giỏ hàng"""
    cart = request.session.get('cart', {})
    prod_id_str = str(product_id)
    if prod_id_str in cart:
        del cart[prod_id_str]
        request.session['cart'] = cart
        request.session.modified = True
        messages.info(request, "Đã xóa mô hình khỏi giỏ hàng.")
    return redirect('shops:cart')


def checkout(request):
    """Trang thanh toán & đặt hàng hoàn chỉnh chuẩn sàn TMĐT cao cấp"""
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Giỏ hàng của bạn đang trống. Hãy chọn mô hình yêu thích nhé!")
        return redirect('shops:home')

    cart_items = []
    total_price = 0
    for product_id, qty in cart.items():
        try:
            prod = Product.objects.get(id=int(product_id))
            subtotal = prod.price * qty
            total_price += subtotal
            cart_items.append({
                'product': prod,
                'quantity': qty,
                'subtotal': subtotal,
            })
        except (Product.DoesNotExist, ValueError):
            continue

    coupon_code = request.session.get('coupon_code')
    coupon_info = COUPONS.get(coupon_code) if coupon_code else None
    discount_amount = 0
    if coupon_info:
        if coupon_info['type'] == 'fixed':
            discount_amount = min(coupon_info['value'], total_price)
        elif coupon_info['type'] == 'percent':
            discount_amount = int(total_price * (coupon_info['value'] / 100))

    has_freeship = (total_price >= 500000 or (coupon_info and coupon_info['type'] == 'freeship'))
    base_shipping_fee = 0 if has_freeship else 30000

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        province = request.POST.get('province', '').strip()
        district = request.POST.get('district', '').strip()
        ward = request.POST.get('ward', '').strip()
        street_address = request.POST.get('address', '').strip()
        address_type = request.POST.get('address_type', 'home')
        delivery_time = request.POST.get('delivery_time', 'any')
        note = request.POST.get('note', '').strip()
        packaging_tags = request.POST.getlist('packaging_tags')
        vat_requested = request.POST.get('vat_requested') == '1'
        vat_company = request.POST.get('vat_company', '').strip()
        vat_tax_code = request.POST.get('vat_tax_code', '').strip()
        vat_email = request.POST.get('vat_email', '').strip()
        payment_method = request.POST.get('payment_method', 'cod')
        shipping_method = request.POST.get('shipping_method', 'standard')

        # Kiểm tra dữ liệu hợp lệ
        if not full_name or not phone or not street_address:
            messages.error(request, "Vui lòng điền đầy đủ Họ tên, Số điện thoại và Địa chỉ giao hàng!")
            return redirect('shops:checkout')

        clean_phone = ''.join(c for c in phone if c.isdigit())
        if len(clean_phone) < 9 or len(clean_phone) > 12:
            messages.error(request, "Số điện thoại nhận hàng không hợp lệ (vui lòng nhập 10 số đúng định dạng)!")
            return redirect('shops:checkout')

        # Ghép địa chỉ đầy đủ & chi tiết
        address_parts = [street_address]
        if ward:
            address_parts.append(ward)
        if district:
            address_parts.append(district)
        if province:
            address_parts.append(province)

        addr_type_labels = {'home': 'Nhà riêng', 'office': 'Cơ quan / Văn phòng'}
        time_labels = {
            'any': 'Giao linh hoạt',
            'office_hours': 'Giờ hành chính (8h00 - 17h30)',
            'weekend': 'Buổi tối / Cuối tuần'
        }
        meta_tag = f"[{addr_type_labels.get(address_type, 'Nhà riêng')} | {time_labels.get(delivery_time, 'Linh hoạt')}]"
        full_address = ", ".join(address_parts) + " " + meta_tag

        # Ghép ghi chú đóng gói, VAT và yêu cầu đặc biệt
        note_parts = []
        if note:
            note_parts.append(f"Ghi chú: {note}")
        if packaging_tags:
            note_parts.append(f"Yêu cầu đóng gói: {', '.join(packaging_tags)}")
        if vat_requested and vat_tax_code:
            note_parts.append(f"Xuất hóa đơn VAT: Cty {vat_company} - MST {vat_tax_code} - Email {vat_email}")
        full_note = " | ".join(note_parts)

        # Tính phí ship chuẩn xác theo phương thức
        if shipping_method == 'express':
            # Hỏa tốc Nika 24h: 55k hoặc 25k nếu đã được freeship chuẩn
            shipping_fee = 25000 if has_freeship else 55000
        elif shipping_method == 'economy':
            # Tiết kiệm đường biển: 20k hoặc miễn phí nếu >= 500k
            shipping_fee = 0 if has_freeship else 20000
        else:
            # Tiêu chuẩn: 30k hoặc miễn phí nếu >= 500k
            shipping_fee = base_shipping_fee

        final_total = max(0, total_price - discount_amount + shipping_fee)

        # Tạo mã đơn hàng độc nhất: OP-XXXXXX
        order_code = f"OP-{uuid.uuid4().hex[:6].upper()}"
        order = Order.objects.create(
            order_code=order_code,
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            phone=clean_phone,
            email=email if email else None,
            address=full_address,
            note=full_note,
            payment_method=payment_method,
            shipping_method=shipping_method,
            coupon_code=coupon_code if coupon_code else None,
            discount_amount=discount_amount,
            shipping_fee=shipping_fee,
            total_price=final_total,
            status='pending',
        )

        # Tạo các mục sản phẩm trong đơn hàng
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                product_name=item['product'].name,
                price=item['product'].price,
                quantity=item['quantity'],
            )

        # Xóa giỏ hàng & coupon sau khi đặt hàng thành công
        request.session['cart'] = {}
        request.session.pop('coupon_code', None)
        request.session.modified = True

        messages.success(request, f"🎉 Chúc mừng Nakama! Đặt hàng thành công với mã đơn #{order.order_code}")
        return redirect('shops:order_success', order_code=order.order_code)

    # Hiển thị form thanh toán
    final_total = max(0, total_price - discount_amount + base_shipping_fee)
    default_name = ''
    default_email = ''
    default_phone = ''
    if request.user.is_authenticated:
        default_name = request.user.first_name or request.user.username
        default_email = request.user.email or ''
        if hasattr(request.user, 'profile'):
            default_phone = request.user.profile.phone or ''

    # Tính các mức phí ship cho giao diện hiển thị động
    fee_standard = 0 if has_freeship else 30000
    fee_express = 25000 if has_freeship else 55000
    fee_economy = 0 if has_freeship else 20000

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'discount_amount': discount_amount,
        'coupon_code': coupon_code,
        'coupon_info': coupon_info,
        'has_freeship': has_freeship,
        'shipping_fee': base_shipping_fee,
        'fee_standard': fee_standard,
        'fee_express': fee_express,
        'fee_economy': fee_economy,
        'final_total': final_total,
        'default_name': default_name,
        'default_email': default_email,
        'default_phone': default_phone,
        'coupons_list': COUPONS,
    }
    return render(request, 'cua_hang/thanh_toan.html', context)


def order_success(request, order_code):
    """Trang xác nhận đặt hàng thành công và cổng thanh toán tự động VietQR (MBBank), MoMo, ZaloPay"""
    order = get_object_or_404(Order, order_code=order_code)

    # 1. Thông tin tài khoản chủ shop
    account_name = "MAI NGUYEN HONG ANH"
    mbbank_account = "12129122006"

    # 2. Tạo link mã VietQR động theo chuẩn Napas MB Bank (tự điền số tiền và mã đơn hàng)
    qr_url = None
    if order.payment_method == 'bank_transfer':
        qr_url = f"https://img.vietqr.io/image/MB-{mbbank_account}-compact2.png?amount={order.total_price}&addInfo={order.order_code}&accountName=MAI%20NGUYEN%20HONG%20ANH"

    # 3. Đường dẫn các ảnh QR thanh toán chính thức
    qr_mbbank_img = "/static/hinh_anh/thanh_toan/qr_mbbank.jpg"
    momo_qr_img = "/static/hinh_anh/thanh_toan/qr_momo.jpg"
    zalopay_qr_img = "/static/hinh_anh/thanh_toan/qr_zalopay.jpg"

    # 4. Thời gian ước tính nhận hàng
    delivery_estimates = {
        'express': 'Trong vòng 24 Giờ (Giao hỏa tốc Nika siêu tốc)',
        'standard': 'Từ 2 - 4 Ngày làm việc (Giao Hàng Tiết Kiệm / Viettel Post)',
        'economy': 'Từ 4 - 6 Ngày làm việc (Đường biển Going Merry)',
    }
    estimated_delivery = delivery_estimates.get(order.shipping_method, 'Từ 2 - 4 Ngày làm việc')

    context = {
        'order': order,
        'account_name': account_name,
        'mbbank_account': mbbank_account,
        'qr_url': qr_url,
        'qr_mbbank_img': qr_mbbank_img,
        'momo_qr_img': momo_qr_img,
        'zalopay_qr_img': zalopay_qr_img,
        'estimated_delivery': estimated_delivery,
    }
    return render(request, 'cua_hang/dat_hang_thanh_cong.html', context)
