-- ===================================================================================
-- HỆ QUẢN TRỊ CƠ SỞ DỮ LIỆU: MySQL / MariaDB (Engine: InnoDB, Charset: utf8mb4)
-- DỰ ÁN: HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ (E-COMMERCE SYSTEM)
-- MÔ TẢ: BẢN THIẾT KẾ CƠ SỞ DỮ LIỆU MỨC VẬT LÝ & DỮ LIỆU MẪU
-- ===================================================================================

-- 1. KHỞI TẠO CƠ SỞ DỮ LIỆU
CREATE DATABASE IF NOT EXISTS `ecommerce_db` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE `ecommerce_db`;

-- Thiết lập bảng mã utf8mb4 cho kết nối để tránh lỗi font tiếng Việt
SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';
SET CHARACTER SET utf8mb4;

-- Tắt kiểm tra khóa ngoại tạm thời để xóa/tạo lại nếu cần làm mới
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `order_items`;
DROP TABLE IF EXISTS `orders`;
DROP TABLE IF EXISTS `products`;
DROP TABLE IF EXISTS `categories`;
DROP TABLE IF EXISTS `user_profiles`;
DROP TABLE IF EXISTS `users`;
SET FOREIGN_KEY_CHECKS = 1;

-- ===================================================================================
-- 2. ĐỊNH NGHĨA CẤU TRÚC BẢNG (TABLE SCHEMAS & CONSTRAINTS)
-- ===================================================================================

-- 2.1. BẢNG NGƯỜI DÙNG CỐT LÕI (users)
-- Lưu trữ thông tin tài khoản đăng nhập & định danh người dùng
CREATE TABLE `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(150) NOT NULL UNIQUE COMMENT 'Tên đăng nhập duy nhất',
    `password` VARCHAR(255) NOT NULL COMMENT 'Mật khẩu đã được mã hóa băm',
    `email` VARCHAR(254) NOT NULL UNIQUE COMMENT 'Địa chỉ email liên hệ',
    `first_name` VARCHAR(150) DEFAULT '' COMMENT 'Tên',
    `last_name` VARCHAR(150) DEFAULT '' COMMENT 'Họ và tên đệm',
    `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '1: Hoạt động, 0: Khóa tài khoản',
    `is_staff` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'Quyền truy cập trang quản trị',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm đăng ký',
    `last_login` DATETIME NULL COMMENT 'Lần đăng nhập gần nhất'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Bảng tài khoản người dùng';

-- 2.2. BẢNG HỒ SƠ & PHÂN QUYỀN MỞ RỘNG (user_profiles)
-- Mối quan hệ 1 - 1 với users, mở rộng vai trò (buyer, seller, admin) và thông tin shop
CREATE TABLE `user_profiles` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL UNIQUE COMMENT 'Khóa ngoại liên kết 1-1 với users',
    `role` ENUM('buyer', 'seller', 'admin') NOT NULL DEFAULT 'buyer' COMMENT 'Vai trò: người mua, người bán, quản trị viên',
    `phone` VARCHAR(20) NULL COMMENT 'Số điện thoại liên hệ',
    `shop_name` VARCHAR(150) NULL COMMENT 'Tên cửa hàng nếu là người bán',
    `avatar` VARCHAR(500) DEFAULT 'https://api.dicebear.com/7.x/bottts/svg?seed=Nakama' COMMENT 'Đường dẫn ảnh đại diện',
    `bio` TEXT NULL COMMENT 'Mô tả ngắn hoặc thông tin giới thiệu',
    `address` TEXT NULL COMMENT 'Địa chỉ mặc định của người dùng',
    CONSTRAINT `fk_profile_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Hồ sơ mở rộng và phân vai trò người dùng';

-- 2.3. BẢNG DANH MỤC SẢN PHẨM (categories)
-- Lưu trữ các nhóm/chủ đề sản phẩm
CREATE TABLE `categories` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL COMMENT 'Tên danh mục sản phẩm',
    `slug` VARCHAR(100) NOT NULL UNIQUE COMMENT 'Đường dẫn thân thiện (SEO Slug)',
    `icon` VARCHAR(50) DEFAULT 'fa-box' COMMENT 'Icon hiển thị danh mục',
    `description` TEXT NULL COMMENT 'Mô tả tóm tắt về danh mục'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Bảng danh mục sản phẩm';

-- 2.4. BẢNG SẢN PHẨM (products)
-- Lưu trữ chi tiết mặt hàng, giá cả, thông số kỹ thuật, người bán và bộ ảnh 4 góc độ
CREATE TABLE `products` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `category_id` BIGINT NOT NULL COMMENT 'Khóa ngoại liên kết danh mục',
    `seller_id` INT NULL COMMENT 'Khóa ngoại liên kết người bán (users)',
    `name` VARCHAR(200) NOT NULL COMMENT 'Tên sản phẩm / mô hình',
    `slug` VARCHAR(200) NOT NULL UNIQUE COMMENT 'Slug thân thiện URL',
    `price` INT NOT NULL COMMENT 'Giá bán hiện tại (VNĐ)',
    `original_price` INT NULL COMMENT 'Giá gốc trước khi giảm (VNĐ)',
    `height` VARCHAR(50) DEFAULT '20 cm' COMMENT 'Chiều cao',
    `scale` VARCHAR(50) DEFAULT 'Tỷ lệ 1/7' COMMENT 'Tỷ lệ kích thước',
    `material` VARCHAR(100) DEFAULT 'PVC cao cấp' COMMENT 'Chất liệu chế tác',
    `brand` VARCHAR(100) DEFAULT 'Chính Hãng' COMMENT 'Thương hiệu / Nhà sản xuất',
    `weight` VARCHAR(50) DEFAULT '800g' COMMENT 'Trọng lượng đóng gói',
    `description` LONGTEXT NULL COMMENT 'Mô tả chi tiết sản phẩm',
    `image` VARCHAR(500) NOT NULL COMMENT 'Ảnh đại diện chính của sản phẩm',
    `image_2` VARCHAR(500) NULL COMMENT 'Ảnh góc chụp 2 (Góc nghiêng/chi tiết)',
    `image_3` VARCHAR(500) NULL COMMENT 'Ảnh góc chụp 3 (Mặt sau/hiệu ứng)',
    `image_4` VARCHAR(500) NULL COMMENT 'Ảnh góc chụp 4 (Hộp sản phẩm Box chính hãng)',
    `in_stock` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '1: Còn hàng, 0: Tạm hết hàng',
    `is_featured` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '1: Sản phẩm nổi bật (HOT), 0: Bình thường',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm đăng sản phẩm',
    INDEX `idx_products_category` (`category_id`),
    INDEX `idx_products_seller` (`seller_id`),
    INDEX `idx_products_featured` (`is_featured`),
    CONSTRAINT `fk_product_category` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_product_seller` FOREIGN KEY (`seller_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Bảng sản phẩm chi tiết';

-- 2.5. BẢNG ĐƠN HÀNG (orders)
-- Lưu trữ hóa đơn bán lẻ, giao dịch thanh toán và thông tin giao nhận
CREATE TABLE `orders` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `order_code` VARCHAR(20) NOT NULL UNIQUE COMMENT 'Mã đơn hàng duy nhất (Ví dụ: OP98231)',
    `user_id` INT NULL COMMENT 'Khóa ngoại liên kết người đặt mua (có thể NULL nếu mua ẩn danh)',
    `full_name` VARCHAR(150) NOT NULL COMMENT 'Họ tên người nhận hàng',
    `phone` VARCHAR(20) NOT NULL COMMENT 'Số điện thoại nhận hàng',
    `email` VARCHAR(254) NULL COMMENT 'Email nhận thông báo đơn hàng',
    `address` TEXT NOT NULL COMMENT 'Địa chỉ giao hàng chi tiết',
    `note` TEXT NULL COMMENT 'Ghi chú thêm từ khách hàng',
    `payment_method` VARCHAR(30) NOT NULL DEFAULT 'cod' COMMENT 'Hình thức thanh toán (cod, bank_transfer, momo, zalopay, credit_card)',
    `shipping_method` VARCHAR(50) NOT NULL DEFAULT 'standard' COMMENT 'Gói vận chuyển (standard, express, economy)',
    `coupon_code` VARCHAR(50) NULL COMMENT 'Mã giảm giá đã áp dụng',
    `discount_amount` INT NOT NULL DEFAULT 0 COMMENT 'Số tiền được giảm giá (VNĐ)',
    `shipping_fee` INT NOT NULL DEFAULT 0 COMMENT 'Phí vận chuyển (VNĐ)',
    `total_price` INT NOT NULL DEFAULT 0 COMMENT 'Tổng số tiền thanh toán cuối cùng (VNĐ)',
    `status` ENUM('pending', 'confirmed', 'shipping', 'completed', 'cancelled') NOT NULL DEFAULT 'pending' COMMENT 'Trạng thái xử lý đơn hàng',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm đặt đơn',
    INDEX `idx_orders_user` (`user_id`),
    INDEX `idx_orders_status` (`status`),
    INDEX `idx_orders_created_at` (`created_at`),
    CONSTRAINT `fk_order_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Bảng đơn hàng';

-- 2.6. BẢNG CHI TIẾT ĐƠN HÀNG (order_items)
-- Mối quan hệ 1 - N với orders, N - 1 với products (Lưu trữ các món hàng trong đơn)
CREATE TABLE `order_items` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `order_id` BIGINT NOT NULL COMMENT 'Khóa ngoại liên kết đơn hàng',
    `product_id` BIGINT NULL COMMENT 'Khóa ngoại liên kết sản phẩm (SET NULL nếu sản phẩm bị gỡ)',
    `product_name` VARCHAR(200) NOT NULL COMMENT 'Tên sản phẩm tại thời điểm mua (bảo lưu lịch sử)',
    `price` INT NOT NULL COMMENT 'Đơn giá tại thời điểm đặt hàng (VNĐ)',
    `quantity` INT UNSIGNED NOT NULL DEFAULT 1 COMMENT 'Số lượng sản phẩm đặt mua',
    INDEX `idx_items_order` (`order_id`),
    INDEX `idx_items_product` (`product_id`),
    CONSTRAINT `fk_item_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_item_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Bảng chi tiết từng mặt hàng trong đơn';

-- ===================================================================================
-- 3. CHÈN DỮ LIỆU MẪU ĐỂ KIỂM THỬ (SEED SAMPLE DATA)
-- ===================================================================================

-- 3.1. Dữ liệu tài khoản users
INSERT INTO `users` (`id`, `username`, `password`, `email`, `first_name`, `last_name`, `is_active`, `is_staff`) VALUES
(1, 'admin', 'pbkdf2_sha256$870000$testpassword$adminhashed', 'admin@onepiecestore.vn', 'Quản Trị', 'Hệ Thống', 1, 1),
(2, 'seller_wano', 'pbkdf2_sha256$870000$testpassword$sellerhashed', 'seller@wano.vn', 'Zoro', 'Roronoa', 1, 0),
(3, 'khachhang01', 'pbkdf2_sha256$870000$testpassword$buyerhashed', 'khachhang01@gmail.com', 'Luffy', 'Monkey D.', 1, 0);

-- 3.2. Dữ liệu hồ sơ user_profiles
INSERT INTO `user_profiles` (`user_id`, `role`, `phone`, `shop_name`, `avatar`, `bio`) VALUES
(1, 'admin', '0901234567', 'Ban Quản Trị Hệ Thống', 'https://api.dicebear.com/7.x/bottts/svg?seed=Admin', 'Quản trị viên toàn hệ thống sàn'),
(2, 'seller', '0988776655', 'Wano Kuni Figure Shop', 'https://api.dicebear.com/7.x/bottts/svg?seed=Zoro', 'Chuyên cung cấp mô hình chính hãng Nhật Bản'),
(3, 'buyer', '0912334455', NULL, 'https://api.dicebear.com/7.x/bottts/svg?seed=Luffy', 'Khách hàng thân thiết đam mê sưu tầm');

-- 3.3. Dữ liệu danh mục categories
INSERT INTO `categories` (`id`, `name`, `slug`, `icon`, `description`) VALUES
(1, 'Băng Mũ Rơm', 'bang-mu-rom', 'fa-hat-cowboy', 'Các nhân vật thuộc băng hải tặc Mũ Rơm'),
(2, 'Tứ Hoàng & Hải Tặc', 'tu-hoang-hai-tac', 'fa-skull-crossbones', 'Các thuyền trưởng vĩ đại và Tứ Hoàng trên đại hải trình'),
(3, 'Hải Quân & Chính Phủ', 'hai-quan-chinh-phu', 'fa-shield-halved', 'Đô Đốc, Trung Tướng và lực lượng Chính Phủ Thế Giới');

-- 3.4. Dữ liệu sản phẩm products
INSERT INTO `products` (`id`, `category_id`, `seller_id`, `name`, `slug`, `price`, `original_price`, `height`, `scale`, `material`, `brand`, `weight`, `description`, `image`, `is_featured`, `in_stock`) VALUES
(1, 1, 2, 'Mô hình Monkey D. Luffy - Gear 5 Nika Thần Mặt Trời', 'mo-hinh-luffy-gear-5-nika', 1250000, 1500000, '28 cm', 'Tỷ lệ 1/6', 'PVC/Resin cao cấp', 'Bandai Spirits', '1.2 kg', 'Mô hình Luffy trạng thái Thức tỉnh Nika với hiệu ứng mây khói tinh xảo sống động.', 'https://images.unsplash.com/photo-1563089145-599997674d42?w=800', 1, 1),
(2, 1, 2, 'Mô hình Roronoa Zoro - Tam Kiếm Phái Asura Quỷ Khí', 'mo-hinh-zoro-asura', 1100000, 1350000, '25 cm', 'Tỷ lệ 1/7', 'PVC cao cấp', 'MegaHouse P.O.P', '950g', 'Mô hình Zoro xuất chiêu Asura Quỷ Khí với 3 thanh bảo kiếm Wado Ichimonji, Sandai Kitetsu, Enma.', 'https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=800', 1, 1),
(3, 2, 2, 'Mô hình Shanks Tóc Đỏ - Bá Khí Ngút Trời Haki Hoàng Gia', 'mo-hinh-shanks-toc-do', 1450000, 1700000, '30 cm', 'Tỷ lệ 1/6', 'Resin & Polystone', 'Banpresto', '1.5 kg', 'Tứ hoàng Shanks uy nghiêm trong trang phục áo choàng đen và thanh kiếm Gryphon.', 'https://images.unsplash.com/photo-1579783902614-a3fb3927b675?w=800', 1, 1);

-- 3.5. Dữ liệu đơn hàng orders
INSERT INTO `orders` (`id`, `order_code`, `user_id`, `full_name`, `phone`, `email`, `address`, `note`, `payment_method`, `shipping_method`, `discount_amount`, `shipping_fee`, `total_price`, `status`) VALUES
(1, 'OP20261001', 3, 'Monkey D. Luffy', '0912334455', 'khachhang01@gmail.com', 'Số 10 Đường Grand Line, Phường Bến Nghé, Quận 1, TP.HCM', 'Giao giờ hành chính, gọi trước 15 phút', 'cod', 'express', 50000, 30000, 1230000, 'confirmed');

-- 3.6. Dữ liệu chi tiết đơn hàng order_items
INSERT INTO `order_items` (`id`, `order_id`, `product_id`, `product_name`, `price`, `quantity`) VALUES
(1, 1, 1, 'Mô hình Monkey D. Luffy - Gear 5 Nika Thần Mặt Trời', 1250000, 1);
