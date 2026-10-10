# 🛠️ CẤU HÌNH HIỂN THỊ DỮ LIỆU TRÊN TRANG QUẢN TRỊ DJANGO ADMIN
import json
from datetime import timedelta
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.db.models import Sum, Count
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Product, Order, OrderItem

# ==========================================
# CẤU HÌNH TRANG QUẢN TRỊ ONE PIECE
# ==========================================
admin.site.site_header = "🏴‍☠️ ONE PIECE FIGURE - QUẢN TRỊ VIÊN"
admin.site.site_title = "One Piece Figure Admin"
admin.site.index_title = "⛵ BẢNG ĐIỀU KHIỂN & THỐNG KÊ KINH DOANH ĐẠI HẢI TRÌNH"

# Tối ưu custom_each_context: Thống kê sinh động tại Dashboard Index
original_each_context = admin.site.each_context

def custom_each_context(request):
    context = original_each_context(request)
    if request.path == reverse('admin:index'):
        total_revenue = Order.objects.exclude(status='cancelled').aggregate(total=Sum('total_price'))['total'] or 0
        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status='pending').count()
        confirmed_orders = Order.objects.filter(status='confirmed').count()
        shipping_orders = Order.objects.filter(status='shipping').count()
        completed_orders = Order.objects.filter(status='completed').count()
        cancelled_orders = Order.objects.filter(status='cancelled').count()

        total_products = Product.objects.count()
        in_stock_products = Product.objects.filter(in_stock=True).count()
        out_of_stock_products = total_products - in_stock_products

        total_categories = Category.objects.count()
        total_customers = User.objects.filter(is_staff=False).count()
        total_users = User.objects.count()

        # Thống kê doanh thu 7 ngày gần nhất
        today = timezone.now().date()
        day_labels = []
        day_revenues = []
        for i in range(6, -1, -1):
            d = today - timedelta(days=i)
            day_labels.append(d.strftime('%d/%m'))
            rev = Order.objects.filter(created_at__date=d).exclude(status='cancelled').aggregate(total=Sum('total_price'))['total'] or 0
            day_revenues.append(rev)

        status_labels = ['Chờ xử lý', 'Đã xác nhận', 'Đang giao', 'Hoàn thành', 'Đã hủy']
        status_counts = [pending_orders, confirmed_orders, shipping_orders, completed_orders, cancelled_orders]

        context.update({
            'kpi_total_revenue': total_revenue,
            'kpi_total_orders': total_orders,
            'kpi_pending_orders': pending_orders,
            'kpi_confirmed_orders': confirmed_orders,
            'kpi_shipping_orders': shipping_orders,
            'kpi_completed_orders': completed_orders,
            'kpi_cancelled_orders': cancelled_orders,
            'kpi_total_products': total_products,
            'kpi_in_stock_products': in_stock_products,
            'kpi_out_of_stock_products': out_of_stock_products,
            'kpi_total_categories': total_categories,
            'kpi_total_customers': total_customers if total_customers > 0 else total_users,
            'recent_orders': Order.objects.order_by('-created_at')[:6],
            'hot_products': Product.objects.filter(is_featured=True)[:6],
            'chart_day_labels_json': json.dumps(day_labels),
            'chart_day_revenues_json': json.dumps(day_revenues),
            'chart_status_labels_json': json.dumps(status_labels),
            'chart_status_counts_json': json.dumps(status_counts),
        })
    return context

admin.site.each_context = custom_each_context


# ==========================================
# 1. DANH MỤC SẢN PHẨM (CATEGORY)
# ==========================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon_preview', 'get_product_count']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        # Tối ưu truy vấn đếm sản phẩm bằng annotate
        return super().get_queryset(request).annotate(total_products=Count('products'))

    @admin.display(description="Icon", ordering='icon')
    def icon_preview(self, obj):
        icon_class = obj.icon if getattr(obj, 'icon', None) else 'fa-box'
        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<i class="fa-solid {}" style="font-size: 1.2rem; color: #e63946;"></i>'
            '<span style="color: #6b7280; font-size: 0.85rem;">{}</span>'
            '</div>',
            icon_class, icon_class
        )

    @admin.display(description="Số mô hình", ordering='total_products')
    def get_product_count(self, obj):
        return format_html(
            '<span style="background: #edf2f7; color: #2d3748; padding: 3px 10px; border-radius: 12px; font-weight: 600;">'
            '{} mẫu</span>',
            obj.total_products
        )


# ==========================================
# 2. SẢN PHẨM / MÔ HÌNH (PRODUCT)
# ==========================================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'category', 'formatted_price', 'scale', 'height', 'is_featured_badge', 'in_stock_badge']
    list_filter = ['category', 'is_featured', 'in_stock', 'brand']
    list_editable = []  # Bỏ list_editable trực tiếp để tránh click nhầm, dùng Actions bên dưới
    search_fields = ['name', 'description', 'brand']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10
    list_select_related = ['category']  # Tối ưu SQL JOIN
    actions = ['make_featured', 'remove_featured', 'make_in_stock', 'make_out_of_stock']

    fieldsets = (
        ('📌 Thông tin cơ bản', {
            'fields': (('name', 'slug'), ('category', 'brand'), 'description')
        }),
        ('💰 Giá & Kho hàng', {
            'fields': (('price', 'in_stock', 'is_featured'),)
        }),
        ('📏 Thông số kỹ thuật Mô hình', {
            'fields': (('scale', 'height'), 'image')
        }),
    )

    @admin.display(description="Hình ảnh")
    def image_preview(self, obj):
        if hasattr(obj, 'image') and obj.image:
            image_url = obj.image.url if hasattr(obj.image, 'url') else obj.image
            return format_html(
                '<img src="{}" style="width: 55px; height: 55px; object-fit: cover; border-radius: 8px; border: 2px solid #ffb703; box-shadow: 0 2px 5px rgba(0,0,0,0.15);" />',
                image_url
            )
        return format_html('<span style="color: #9ca3af; font-style: italic;">Chưa có ảnh</span>')

    @admin.display(description="Giá bán", ordering='price')
    def formatted_price(self, obj):
        return format_html('<span style="color: #059669; font-weight: 700; font-size: 0.95rem;">{:,} đ</span>', obj.price)

    @admin.display(description="Nổi bật", boolean=True)
    def is_featured_badge(self, obj):
        return obj.is_featured

    @admin.display(description="Trạng thái kho", boolean=True)
    def in_stock_badge(self, obj):
        return obj.in_stock

    # Bulk Actions
    @admin.action(description="🔥 Đánh dấu NỔI BẬT (HOT)")
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"Đã đánh dấu Nổi Bật cho {updated} mô hình.")

    @admin.action(description="❌ Bỏ trạng thái Nổi Bật")
    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f"Đã bỏ Nổi Bật của {updated} mô hình.")

    @admin.action(description="✅ Đánh dấu CÒN HÀNG")
    def make_in_stock(self, request, queryset):
        updated = queryset.update(in_stock=True)
        self.message_user(request, f"Đã cập nhật Còn Hàng cho {updated} mô hình.")

    @admin.action(description="⚠️ Đánh dấu HẾT HÀNG")
    def make_out_of_stock(self, request, queryset):
        updated = queryset.update(in_stock=False)
        self.message_user(request, f"Đã cập nhật Hết Hàng cho {updated} mô hình.")


# ==========================================
# 3. CHI TIẾT ĐƠN HÀNG INLINE (ORDER ITEM)
# ==========================================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_preview', 'product_link', 'price', 'quantity', 'get_subtotal']
    fields = ['product_preview', 'product_link', 'price', 'quantity', 'get_subtotal']
    can_delete = False

    @admin.display(description="Ảnh mô hình")
    def product_preview(self, obj):
        if obj.product and getattr(obj.product, 'image', None):
            image_url = obj.product.image.url if hasattr(obj.product.image, 'url') else obj.product.image
            return format_html('<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 6px;" />', image_url)
        return "-"

    @admin.display(description="Sản phẩm")
    def product_link(self, obj):
        if obj.product:
            url = reverse('admin:shops_product_change', args=[obj.product.id])
            return format_html('<a href="{}" style="font-weight: 600; color: #2563eb; text-decoration: none;">{}</a>', url, obj.product.name)
        return obj.product_name if hasattr(obj, 'product_name') else "Sản phẩm đã bị xóa"

    @admin.display(description="Thành tiền")
    def get_subtotal(self, obj):
        if not obj or not obj.id:
            return "-"
        price = obj.price or 0
        qty = obj.quantity or 0
        return format_html('<strong style="color: #059669;">{:,} VNĐ</strong>', price * qty)


# ==========================================
# 4. QUẢN LÝ ĐƠN HÀNG (ORDER)
# ==========================================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_code', 'customer_display', 'phone', 'formatted_total', 'payment_method_badge', 'status_badge', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_code', 'full_name', 'phone', 'email', 'address']
    inlines = [OrderItemInline]
    readonly_fields = ['order_code', 'created_at', 'formatted_total_detail']
    list_per_page = 15
    actions = ['mark_confirmed', 'mark_shipping', 'mark_completed', 'mark_cancelled']

    fieldsets = (
        ('📦 Thông tin Đơn hàng', {
            'fields': (('order_code', 'created_at'), ('status', 'payment_method'))
        }),
        ('👤 Thông tin Khách hàng', {
            'fields': (('user', 'full_name'), ('phone', 'email'), 'address', 'note')
        }),
        ('💳 Thanh toán', {
            'fields': ('formatted_total_detail',)
        }),
    )

    @admin.display(description="Khách hàng", ordering='full_name')
    def customer_display(self, obj):
        if obj.user:
            return format_html('<div><strong>{}</strong><br><small style="color: #6b7280;"><i class="fas fa-user-circle"></i> {}</small></div>', obj.full_name, obj.user.username)
        return format_html('<strong>{}</strong>', obj.full_name)

    @admin.display(description="Tổng tiền", ordering='total_price')
    def formatted_total(self, obj):
        return format_html('<strong style="color: #059669; font-size: 0.95rem;">{:,} VNĐ</strong>', obj.total_price)

    @admin.display(description="Tổng thanh toán")
    def formatted_total_detail(self, obj):
        return format_html('<span style="color: #059669; font-size: 1.2rem; font-weight: bold;">{:,} VNĐ</span>', obj.total_price)

    @admin.display(description="Phương thức thanh toán")
    def payment_method_badge(self, obj):
        if obj.payment_method == 'bank_transfer':
            return format_html(
                '<span style="background: #fef2f2; color: #dc2626; font-weight: 600; padding: 4px 10px; border-radius: 6px; border: 1px solid #fecaca; font-size: 0.8rem;">'
                '<i class="fa-solid fa-qrcode me-1"></i> VietQR</span>'
            )
        return format_html(
            '<span style="background: #fffbeb; color: #d97706; font-weight: 600; padding: 4px 10px; border-radius: 6px; border: 1px solid #fef3c7; font-size: 0.8rem;">'
            '<i class="fa-solid fa-money-bill me-1"></i> COD</span>'
        )

    @admin.display(description="Trạng thái")
    def status_badge(self, obj):
        colors = {
            'pending': ('#fffbe1', '#b45309', '⏳ Chờ Xử Lý'),
            'confirmed': ('#eff6ff', '#1d4ed8', '✅ Đã Xác Nhận'),
            'shipping': ('#f3e8ff', '#6b21a8', '🚚 Đang Giao Hàng'),
            'completed': ('#ecfdf5', '#047857', '🎉 Hoàn Thành'),
            'cancelled': ('#fef2f2', '#b91c1c', '🚫 Đã Hủy'),
        }
        bg, fg, text = colors.get(obj.status, ('#f3f4f6', '#374151', obj.status))
        return format_html(
            '<span style="background: {}; color: {}; font-weight: 700; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; display: inline-block;">{}</span>',
            bg, fg, text
        )

    # Fast Status Change Actions
    @admin.action(description="⚡ Xác nhận đơn hàng đã chọn")
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f"Đã xác nhận {updated} đơn hàng thành công.")

    @admin.action(description="🚚 Chuyển sang Đang giao hàng")
    def mark_shipping(self, request, queryset):
        updated = queryset.update(status='shipping')
        self.message_user(request, f"Đã chuyển {updated} đơn hàng sang trạng thái Đang Giao Hàng.")

    @admin.action(description="🎉 Đánh dấu Đã Hoàn Thành")
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f"Đã chuyển {updated} đơn hàng sang Hoàn Thành.")

    @admin.action(description="🚫 Hủy các đơn hàng đã chọn")
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f"Đã hủy {updated} đơn hàng.")