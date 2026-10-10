# ==============================================================================
# 🗄️ MIỀN CƠ SỞ DỮ LIỆU & ORM / DATABASE & DATA MODELING DOMAIN
# File: cua_hang/co_so_du_lieu.py (và cua_hang/models.py)
# Khai báo cấu trúc 5 bảng dữ liệu cốt lõi của website One Piece Store:
#   1. UserProfile: Mở rộng tài khoản & phân 3 vai trò (buyer, seller, admin)
#   2. Category: Danh mục mô hình One Piece (Băng Mũ Rơm, Tứ Hoàng, Hải Quân...)
#   3. Product: Thông tin mô hình (kích thước, tỷ lệ, giá và hệ thống 4 góc ảnh)
#   4. Order: Hóa đơn đơn hàng (thanh toán COD/VietQR Napas/MoMo, phí ship, voucher)
#   5. OrderItem: Chi tiết từng món mô hình trong đơn hàng
# ==============================================================================

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Hồ sơ mở rộng cho tài khoản: lưu vai trò (buyer, seller, admin), thông tin shop, sđt"""
    ROLE_CHOICES = [
        ('buyer', 'Người mua (Khách hàng)'),
        ('seller', 'Người bán (Chủ gian hàng)'),
        ('admin', 'Quản trị viên web'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='buyer', verbose_name="Vai trò")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số điện thoại")
    shop_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Tên gian hàng / Shop")
    avatar = models.URLField(max_length=500, blank=True, null=True, default="https://api.dicebear.com/7.x/bottts/svg?seed=Nakama", verbose_name="Ảnh đại diện")
    bio = models.TextField(blank=True, null=True, verbose_name="Giới thiệu shop / Ghi chú")

    class Meta:
        verbose_name = "Hồ sơ người dùng"
        verbose_name_plural = "Hồ sơ người dùng"

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    """Tự động tạo hoặc đồng bộ profile khi User được tạo hoặc lưu"""
    if created:
        role = 'admin' if (instance.is_superuser or instance.is_staff) else 'buyer'
        UserProfile.objects.get_or_create(user=instance, defaults={'role': role})
    else:
        if hasattr(instance, 'profile'):
            if (instance.is_superuser or instance.is_staff) and instance.profile.role != 'admin':
                instance.profile.role = 'admin'
                instance.profile.save()
        else:
            role = 'admin' if (instance.is_superuser or instance.is_staff) else 'buyer'
            UserProfile.objects.get_or_create(user=instance, defaults={'role': role})


class Category(models.Model):
    """Bảng danh mục nhân vật / chủ đề One Piece"""
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default="fa-skull-crossbones", verbose_name="Icon FontAwesome")

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Bảng lưu thông tin mô hình One Piece"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Danh mục")
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="Người bán / Chủ shop")
    name = models.CharField(max_length=200, verbose_name="Tên mô hình")
    slug = models.SlugField(unique=True)
    price = models.IntegerField(verbose_name="Giá bán (VNĐ)")
    original_price = models.IntegerField(null=True, blank=True, verbose_name="Giá gốc (VNĐ)")
    height = models.CharField(max_length=50, default="20 cm", verbose_name="Chiều cao")
    scale = models.CharField(max_length=50, default="Tỷ lệ 1/7", verbose_name="Tỷ lệ")
    material = models.CharField(max_length=50, default="PVC cao cấp", verbose_name="Chất liệu")
    brand = models.CharField(max_length=100, default="Bandai / Banpresto", verbose_name="Hãng sản xuất")
    weight = models.CharField(max_length=50, default="850g", verbose_name="Trọng lượng")
    description = models.TextField(blank=True, verbose_name="Mô tả chi tiết")
    
    # 📸 HỆ THỐNG ẢNH CHI TIẾT ĐA GÓC ĐỘ
    image = models.URLField(max_length=500, default="https://via.placeholder.com/600x600", verbose_name="Ảnh chính")
    image_2 = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ảnh chi tiết 2 (Góc nghiêng/Cận cảnh)")
    image_3 = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ảnh chi tiết 3 (Phía sau/Hiệu ứng)")
    image_4 = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ảnh chi tiết 4 (Vỏ hộp Box chính hãng)")
    
    is_featured = models.BooleanField(default=False, verbose_name="Sản phẩm nổi bật / HOT")
    in_stock = models.BooleanField(default=True, verbose_name="Còn hàng")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    class Meta:
        verbose_name = "Mô hình"
        verbose_name_plural = "Danh sách mô hình"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def discount_percent(self):
        """Tính phần trăm giảm giá tự động"""
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    @property
    def all_images(self):
        """Trả về toàn bộ danh sách ảnh của mô hình (lọc bỏ ảnh trống)"""
        imgs = []
        for img in [self.image, self.image_2, self.image_3, self.image_4]:
            if img and str(img).strip():
                imgs.append(str(img).strip())
        return imgs if imgs else [self.image]


class Order(models.Model):
    """Bảng đơn hàng khách đặt"""
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('confirmed', 'Đã xác nhận'),
        ('shipping', 'Đang giao hàng'),
        ('completed', 'Đã hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]

    PAYMENT_CHOICES = [
        ('cod', 'Thanh toán khi nhận hàng (COD)'),
        ('bank_transfer', 'Chuyển khoản VietQR Ngân Hàng'),
        ('momo', 'Ví Điện Tử MoMo'),
        ('zalopay', 'Ví Điện Tử ZaloPay'),
        ('credit_card', 'Thẻ Quốc Tế (Visa/Mastercard)'),
    ]

    SHIPPING_CHOICES = [
        ('standard', 'Giao Tiêu Chuẩn Grand Line (2 - 4 ngày)'),
        ('express', 'Giao Hỏa Tốc Nika Siêu Tốc (24 Giờ)'),
        ('economy', 'Giao Tiết Kiệm Tàu Merry (4 - 6 ngày)'),
    ]

    order_code = models.CharField(max_length=20, unique=True, verbose_name="Mã đơn hàng")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tài khoản khách hàng", related_name="orders")
    full_name = models.CharField(max_length=150, verbose_name="Họ và tên người nhận")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    address = models.TextField(verbose_name="Địa chỉ giao hàng")
    note = models.TextField(blank=True, verbose_name="Ghi chú đơn hàng")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod', verbose_name="Phương thức thanh toán")
    shipping_method = models.CharField(max_length=50, choices=SHIPPING_CHOICES, default='standard', verbose_name="Hình thức vận chuyển")
    coupon_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="Mã giảm giá")
    discount_amount = models.IntegerField(default=0, verbose_name="Số tiền giảm (VNĐ)")
    shipping_fee = models.IntegerField(default=0, verbose_name="Phí vận chuyển (VNĐ)")
    total_price = models.IntegerField(default=0, verbose_name="Tổng tiền thanh toán (VNĐ)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái đơn hàng")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian đặt")

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Danh sách đơn hàng"
        ordering = ['-created_at']

    def __str__(self):
        return f"Đơn hàng #{self.order_code} - {self.full_name}"


class OrderItem(models.Model):
    """Bảng chi tiết các món hàng trong một đơn hàng"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Đơn hàng")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Sản phẩm")
    product_name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    price = models.IntegerField(verbose_name="Đơn giá")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")

    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    @property
    def subtotal(self):
        return (self.price or 0) * (self.quantity or 0)
