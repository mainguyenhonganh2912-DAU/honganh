# ==============================================================================
# 👤 MIỀN TÀI KHOẢN & PHÂN QUYỀN / AUTHENTICATION & IDENTITY DOMAIN
# File: cua_hang/xu_ly_tai_khoan.py
# Chứa toàn bộ các hàm xác thực và quản lý tài khoản người dùng:
#   1. customer_login: Đăng nhập thông minh (tự động điều hướng Buyer, Seller, Admin)
#   2. customer_register: Đăng ký thành viên mới (hỗ trợ cả Người mua & Người bán gian hàng)
#   3. customer_logout: Đăng xuất an toàn
#   4. customer_profile: Hồ sơ cá nhân & theo dõi lịch sử đơn hàng
# Liên kết CSDL: auth_user, UserProfile, Order (trong co_so_du_lieu.py)
# ==============================================================================

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.db.models import Q, Sum
from .models import Order, UserProfile


def customer_login(request):
    """Trang đăng nhập dành cho Khách hàng, Người bán và Quản trị viên"""
    if request.user.is_authenticated:
        # Nếu đã đăng nhập thì chuyển hướng thông minh theo vai trò
        role = getattr(getattr(request.user, 'profile', None), 'role', 'buyer')
        if request.user.is_superuser or request.user.is_staff or role == 'admin':
            return redirect(reverse('shops:admin_portal_dashboard'))
        elif role == 'seller':
            return redirect(reverse('shops:seller_dashboard'))
        return redirect(reverse('shops:home'))

    # Lấy URL chuyển hướng sau đăng nhập (nếu có)
    next_url = request.GET.get('next', '').strip() or request.POST.get('next', '').strip()

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        remember_me = request.POST.get('remember_me')

        if not username or not password:
            messages.error(request, 'Vui lòng nhập đầy đủ Tên đăng nhập và Mật khẩu!')
            return render(request, 'cua_hang/dang_nhap.html', {'next': next_url, 'username': username})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)       # Hết hạn khi đóng trình duyệt
                else:
                    request.session.set_expiry(1209600) # Ghi nhớ 2 tuần

                name_display = user.first_name or user.username
                role = getattr(getattr(user, 'profile', None), 'role', 'buyer')

                # Điều hướng theo vai trò sau khi đăng nhập thành công
                if user.is_superuser or user.is_staff or role == 'admin':
                    messages.success(request, f'Xin chào Admin {name_display}! Chào mừng đến Trung Tâm Quản Trị.')
                    # Ưu tiên chuyển đến next_url nếu hợp lệ
                    if next_url and next_url.startswith('/') and 'dang-nhap' not in next_url:
                        return redirect(next_url)
                    return redirect(reverse('shops:admin_portal_dashboard'))

                elif role == 'seller':
                    shop_name = getattr(getattr(user, 'profile', None), 'shop_name', 'Gian hàng của bạn')
                    messages.success(request, f"Chào mừng Chủ Shop '{shop_name}' ({name_display}) đã trở lại Kênh Người Bán!")
                    if next_url and next_url.startswith('/') and 'dang-nhap' not in next_url:
                        return redirect(next_url)
                    return redirect(reverse('shops:seller_dashboard'))

                else:
                    messages.success(request, f'Chào mừng Nakama {name_display} đã cập bến One Piece Store!')
                    if next_url and next_url.startswith('/') and 'dang-nhap' not in next_url:
                        return redirect(next_url)
                    return redirect(reverse('shops:home'))
            else:
                messages.error(request, 'Tài khoản của bạn hiện đang bị khóa tạm thời.')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không chính xác. Vui lòng kiểm tra lại!')

    return render(request, 'cua_hang/dang_nhap.html', {'next': next_url})


def customer_register(request):
    """Trang đăng ký tài khoản mới: Hỗ trợ chọn vai trò Người mua hoặc Người bán"""
    if request.user.is_authenticated:
        return redirect(reverse('shops:home'))

    if request.method == 'POST':
        role = request.POST.get('role', 'buyer').strip()
        username = request.POST.get('username', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        shop_name = request.POST.get('shop_name', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        form_data = {
            'role': role,
            'username': username,
            'full_name': full_name,
            'email': email,
            'phone': phone,
            'shop_name': shop_name,
        }

        # --- Kiểm tra đầu vào ---
        if not username or not password or not confirm_password:
            messages.error(request, 'Vui lòng điền đầy đủ Tên đăng nhập và Mật khẩu!')
            return render(request, 'cua_hang/dang_ky.html', {'form_data': form_data})

        if len(username) < 4:
            messages.error(request, 'Tên đăng nhập phải có ít nhất 4 ký tự!')
            return render(request, 'cua_hang/dang_ky.html', {'form_data': form_data})

        if len(password) < 6:
            messages.error(request, 'Mật khẩu bảo mật phải có ít nhất 6 ký tự!')
            return render(request, 'cua_hang/dang_ky.html', {'form_data': form_data})

        if password != confirm_password:
            messages.error(request, 'Mật khẩu xác nhận không khớp. Vui lòng nhập lại!')
            return render(request, 'cua_hang/dang_ky.html', {'form_data': form_data})

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, f"Tên tài khoản '{username}' đã tồn tại. Hãy chọn tên khác!")
            return render(request, 'cua_hang/dang_ky.html', {'form_data': form_data})

        if email and User.objects.filter(email__iexact=email).exists():
            messages.error(request, f"Email '{email}' đã được sử dụng cho tài khoản khác!")
            return render(request, 'cua_hang/dang_ky.html', {'form_data': form_data})

        # Nếu đăng ký là người bán, yêu cầu tên shop và số điện thoại
        if role == 'seller':
            if not shop_name:
                shop_name = f'Shop {full_name or username}'
            if not phone:
                messages.error(request, 'Người bán vui lòng cung cấp Số điện thoại để khách hàng liên hệ!')
                return render(request, 'cua_hang/dang_ky.html', {'form_data': form_data})

        # --- Tạo tài khoản User Django ---
        user = User.objects.create_user(
            username=username,
            email=email if email else '',
            password=password,
            first_name=full_name if full_name else username,
        )

        # Cập nhật hồ sơ UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = 'seller' if role == 'seller' else 'buyer'
        profile.phone = phone
        if role == 'seller':
            profile.shop_name = shop_name
        profile.save()

        # Tự động đăng nhập sau khi tạo tài khoản thành công
        auth_login(request, user)

        if role == 'seller':
            messages.success(request, f"Chúc mừng! Gian hàng '{shop_name}' đã được tạo thành công. Hãy bắt đầu đăng bán mô hình!")
            return redirect(reverse('shops:seller_dashboard'))
        else:
            messages.success(request, f'Chào mừng Nakama {user.first_name} đã gia nhập One Piece Store!')
            return redirect(reverse('shops:home'))

    return render(request, 'cua_hang/dang_ky.html', {'form_data': {'role': 'buyer'}})


def customer_logout(request):
    """Đăng xuất tài khoản an toàn"""
    auth_logout(request)
    messages.info(request, 'Bạn đã đăng xuất thành công. Hẹn gặp lại bạn sớm!')
    return redirect(reverse('shops:home'))


# Dùng login_url bằng đường dẫn thực (không phải URL name) vì Django không hỗ trợ namespace ở đây
@login_required(login_url='/dang-nhap/')
def customer_profile(request):
    """Hồ sơ cá nhân và lịch sử đơn hàng của người dùng"""
    orders = Order.objects.filter(
        Q(user=request.user) | (Q(email__isnull=False) & Q(email=request.user.email) & ~Q(email=''))
    ).distinct().order_by('-created_at')

    total_spent = orders.exclude(status='cancelled').aggregate(total=Sum('total_price'))['total'] or 0
    completed_orders = orders.filter(status='completed').count()

    # Cập nhật thông tin tài khoản nếu gửi form POST
    if request.method == 'POST':
        new_name = request.POST.get('full_name', '').strip()
        new_email = request.POST.get('email', '').strip()
        new_phone = request.POST.get('phone', '').strip()

        if new_name:
            request.user.first_name = new_name
        if new_email:
            request.user.email = new_email
        request.user.save()

        if hasattr(request.user, 'profile'):
            if new_phone:
                request.user.profile.phone = new_phone
            request.user.profile.save()

        messages.success(request, 'Cập nhật hồ sơ tài khoản thành công!')
        return redirect(reverse('shops:profile'))

    context = {
        'orders': orders,
        'total_orders': orders.count(),
        'total_spent': total_spent,
        'completed_orders': completed_orders,
    }
    return render(request, 'cua_hang/ho_so_ca_nhan.html', context)
