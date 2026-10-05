# ==============================================================================
# 🌱 FILE NẠP DỮ LIỆU MẪU ĐỒ HỌA SẮC NÉT (seed_data.py)
# Nạp danh mục One Piece và 14 siêu phẩm mô hình có đầy đủ 4 góc ảnh chi tiết
# ==============================================================================
import os
import sys
import django

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'du_an.settings')
django.setup()

from django.contrib.auth.models import User
from cua_hang.models import Category, Product, UserProfile


def run_seed():
    print("🏴‍☠️ Bắt đầu cập nhật dữ liệu mô hình One Piece chân thực sắc nét...")

    # 1. Đảm bảo có tài khoản demo: admin, nguoiban, nguoimua
    admin_user, _ = User.objects.get_or_create(username="admin", defaults={"email": "admin@onepiecestore.vn", "first_name": "Đô Đốc Admin", "is_staff": True, "is_superuser": True})
    admin_user.set_password("admin123")
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    p_admin, _ = UserProfile.objects.get_or_create(user=admin_user)
    p_admin.role = 'admin'
    p_admin.save()

    seller_user, _ = User.objects.get_or_create(username="nguoiban", defaults={"email": "seller@onepiecestore.vn", "first_name": "Chủ Shop Zoro", "is_staff": False, "is_superuser": False})
    seller_user.set_password("seller123")
    seller_user.save()
    p_seller, _ = UserProfile.objects.get_or_create(user=seller_user)
    p_seller.role = 'seller'
    p_seller.shop_name = 'Zoro Swordsman Figure Store'
    p_seller.phone = '0988776655'
    p_seller.save()

    buyer_user, _ = User.objects.get_or_create(username="nguoimua", defaults={"email": "buyer@nakama.vn", "first_name": "Nakama Mua Hàng", "is_staff": False, "is_superuser": False})
    buyer_user.set_password("buyer123")
    buyer_user.is_staff = False
    buyer_user.is_superuser = False
    buyer_user.save()
    p_buyer, _ = UserProfile.objects.get_or_create(user=buyer_user)
    p_buyer.role = 'buyer'
    p_buyer.phone = '0912345678'
    p_buyer.save()

    print("✅ Đã thiết lập xong 3 tài khoản chuẩn: admin / nguoiban / nguoimua")

    # 2. Tạo danh mục
    categories_data = [
        {"name": "Băng Mũ Rơm", "slug": "bang-mu-rom", "icon": "fa-skull"},
        {"name": "Tứ Hoàng & Huyền Thoại", "slug": "tu-hoang-huyen-thoai", "icon": "fa-crown"},
        {"name": "Thất Vũ Hải & Tân Tinh", "slug": "that-vu-hai-sieu-tan-tinh", "icon": "fa-shield-halved"},
        {"name": "Hải Quân & Chính Phủ", "slug": "hai-quan-chinh-phu", "icon": "fa-anchor"},
        {"name": "Mô Hình Resin Cao Cấp GK", "slug": "mo-hinh-resin-gk", "icon": "fa-gem"},
    ]

    cat_objs = {}
    for cdata in categories_data:
        cat, _ = Category.objects.update_or_create(
            slug=cdata["slug"],
            defaults={"name": cdata["name"], "icon": cdata["icon"]}
        )
        cat_objs[cdata["slug"]] = cat

    # 3. Danh sách 14 mô hình One Piece chân thực với 4 góc ảnh chi tiết
    products_data = [
        {
            "name": "Mô Hình Monkey D. Luffy Gear 5 Nika Thần Mặt Trời",
            "slug": "luffy-gear-5-nika-than-mat-troi",
            "category": cat_objs["bang-mu-rom"],
            "seller": seller_user,
            "price": 1450000,
            "original_price": 1800000,
            "height": "28 cm",
            "scale": "Tỷ lệ 1/7",
            "material": "PVC & ABS cao cấp",
            "brand": "Bandai Spirits / Megahouse P.O.P",
            "weight": "1200g",
            "is_featured": True,
            "in_stock": True,
            "image": "/static/hinh_anh/san_pham/luffy_gear5.jpg",
            "image_2": "https://images2.alphacoders.com/131/1312386.jpeg",
            "image_3": "https://wallpapercave.com/wp/wp12480687.jpg",
            "image_4": "https://i.pinimg.com/736x/88/44/22/884422cb4244b706c646b9a89c894564.jpg",
            "description": "Mô hình Luffy trạng thái thức tỉnh Trái Ác Quỷ Zoan Thần Thoại Hito Hito no Mi: Model Nika (Thần Mặt Trời). Tái hiện khoảnh khắc Luffy tươi cười tự do với mái tóc và làn khói mây trắng bồng bềnh trên đỉnh Onigashima. Chi tiết tia sét cầm tay cực kỳ sống động và hiệu ứng lửa tím bao quanh tuyệt mỹ."
        },
        {
            "name": "Mô Hình Roronoa Zoro Tam Kiếm Asura Enma Khát Máu",
            "slug": "roronoa-zoro-tam-kiem-asura-enma",
            "category": cat_objs["bang-mu-rom"],
            "seller": seller_user,
            "price": 1250000,
            "original_price": 1500000,
            "height": "26 cm",
            "scale": "Tỷ lệ 1/8",
            "material": "PVC đúc đặc cao cấp",
            "brand": "Banpresto Grandista Nero",
            "weight": "950g",
            "is_featured": True,
            "in_stock": True,
            "image": "/static/hinh_anh/san_pham/zoro_enma.jpg",
            "image_2": "https://images4.alphacoders.com/132/1325338.jpeg",
            "image_3": "https://wallpapercave.com/wp/wp12001438.jpg",
            "image_4": "https://i.pinimg.com/736x/ec/eb/fa/ecebfa2dbb2c8a98b47bb9be4a0eeeb0.jpg",
            "description": "Zoro trong tư thế xuất chiêu Tuyệt Kỹ Cửu Đao Lưu Asura kết hợp Haki Bá Vương truyền vào Diêm Kiếm Enma. Lưỡi kiếm rực sáng hiệu ứng Haki tím cùng ánh mắt rực lửa sẵn sàng chém gãy cánh Rồng Kaido. Kèm đế hiệu ứng bốc khói đen cực ngầu."
        },
        {
            "name": "Mô Hình Vinsmoke Sanji Ifrit Jambe Chân Lửa Quỷ Xanh",
            "slug": "sanji-ifrit-jambe-chan-lua-quy-xanh",
            "category": cat_objs["bang-mu-rom"],
            "seller": seller_user,
            "price": 890000,
            "original_price": 1100000,
            "height": "24 cm",
            "scale": "Tỷ lệ 1/8",
            "material": "PVC cao cấp đúc khuôn sắc nét",
            "brand": "Bandai Ichiban Kuji Wano",
            "weight": "850g",
            "is_featured": True,
            "in_stock": True,
            "image": "/static/hinh_anh/san_pham/sanji_ifrit.jpg",
            "image_2": "https://images8.alphacoders.com/133/1338575.png",
            "image_3": "https://wallpapercave.com/wp/wp12242137.jpg",
            "image_4": "https://i.pinimg.com/736x/bc/62/1d/bc621d9600e123fc474a004eb7c9ebec.jpg",
            "description": "Chiến binh tóc vàng của Băng Mũ Rơm với bộ đồ Stealth Black cải tiến và tuyệt kỹ chân lửa xanh Ifrit Jambe. Ánh lửa plasma xanh siêu nóng kết hợp cùng bộ xương ngoại tộc Germa bất hoại đánh bay Queen Bệnh Dịch."
        },
        {
            "name": "Mô Hình Tứ Hoàng Shanks Tóc Đỏ Tuyệt Kỹ Kamusari",
            "slug": "tu-hoang-shanks-toc-do-kamusari",
            "category": cat_objs["tu-hoang-huyen-thoai"],
            "seller": seller_user,
            "price": 1690000,
            "original_price": 2100000,
            "height": "30 cm",
            "scale": "Tỷ lệ 1/7",
            "material": "PVC & Resin hiệu ứng chớp đen",
            "brand": "Megahouse P.O.P (Portrait.Of.Pirates)",
            "weight": "1400g",
            "is_featured": True,
            "in_stock": True,
            "image": "/static/hinh_anh/san_pham/shanks_figure.jpg",
            "image_2": "https://images5.alphacoders.com/132/1328405.jpeg",
            "image_3": "https://wallpapercave.com/wp/wp11400262.jpg",
            "image_4": "https://i.pinimg.com/736x/8f/c9/2a/8fc92a2a0ff9e07d0cebfaec2cb84ef7.jpg",
            "description": "Tứ Hoàng Shanks Tóc Đỏ tuốt thanh danh kiếm Gryphon tung ra đòn Kamusari (Thần Xung) từng là tuyệt chiêu của Vua Hải Tặc Roger. Haki Bá Vương tỏa ra chớp đen dữ dội đánh gục thuyền trưởng Kid chỉ trong một đòn chém duy nhất."
        },
        {
            "name": "Mô Hình Tứ Hoàng Kaido Bách Thú Long Hóa Hào Khí",
            "slug": "kaido-bach-thu-long-hoa-hao-khi",
            "category": cat_objs["tu-hoang-huyen-thoai"],
            "seller": seller_user,
            "price": 2850000,
            "original_price": 3400000,
            "height": "38 cm",
            "scale": "Tỷ lệ 1/6 Khổng Lồ",
            "material": "PVC & ABS đúc khối nguyên khối",
            "brand": "Bandai Tamashii Nations Extra Battle",
            "weight": "3200g",
            "is_featured": True,
            "in_stock": True,
            "image": "/static/hinh_anh/san_pham/kaido_figure.jpg",
            "image_2": "https://images4.alphacoders.com/129/1297125.png",
            "image_3": "https://wallpapercave.com/wp/wp10352528.jpg",
            "image_4": "https://i.pinimg.com/736x/32/34/09/32340984852932f913d80bc0eb2a79ee.jpg",
            "description": "Sinh vật mạnh nhất thế giới Kaido trong dạng Bán Long kết hợp Chùy Hassaikai sấm sét bao phủ. Thân rồng vảy xanh uốn lượn hùng tráng với sừng sững bão lửa, chi tiết vân vảy và cơ bắp cuồn cuộn đáng kinh ngạc."
        },
        {
            "name": "Mô Hình Râu Trắng Edward Newgate Đại Chiến Marineford",
            "slug": "rau-trang-edward-newgate-marineford",
            "category": cat_objs["tu-hoang-huyen-thoai"],
            "seller": seller_user,
            "price": 2200000,
            "original_price": 2700000,
            "height": "34 cm",
            "scale": "Tỷ lệ 1/7",
            "material": "PVC cao cấp",
            "brand": "Megahouse Maximum",
            "weight": "2100g",
            "is_featured": True,
            "in_stock": True,
            "image": "/static/hinh_anh/san_pham/whitebeard.png",
            "image_2": "https://images3.alphacoders.com/133/1338879.png",
            "image_3": "https://wallpapercave.com/wp/wp8333240.jpg",
            "image_4": "https://i.pinimg.com/736x/95/8e/3c/958e3cb2726330cefa0c0e5a8742512a.jpg",
            "description": "Người đàn ông mạnh nhất thế giới Edward Newgate với đại đao Murakumogiri và chiêu thức Rung Chấn nứt vỡ không gian tại Tổng Bộ Hải Quân Marineford. Thần thái oai nghiêm kiêu hùng không một vết thương sau lưng."
        },
        {
            "name": "Mô Hình Hỏa Quyền Portgas D. Ace Đại Hỏa Xà Hỏa Đế",
            "slug": "hoa-quyen-portgas-d-ace-dai-hoa-xa",
            "category": cat_objs["tu-hoang-huyen-thoai"],
            "seller": seller_user,
            "price": 950000,
            "original_price": 1200000,
            "height": "25 cm",
            "scale": "Tỷ lệ 1/8",
            "material": "PVC & Resin lửa trong suốt",
            "brand": "Bandai Spirits Figuarts ZERO",
            "weight": "900g",
            "is_featured": True,
            "in_stock": True,
            "image": "/static/hinh_anh/san_pham/ace_fire.jpg",
            "image_2": "https://images6.alphacoders.com/132/1328325.png",
            "image_3": "https://wallpapercave.com/wp/wp9298418.jpg",
            "image_4": "https://i.pinimg.com/736x/a2/4b/32/a24b32b2b1d7d0669298cf1ebcb23ec4.jpg",
            "description": "Đội trưởng Đội 2 Băng Râu Trắng Portgas D. Ace xuất chiêu Hỏa Quyền bốc lửa bao quanh cơ thể. Mũ cao bồi hạt đỏ, hình xăm Whitebeard sau lưng và ánh mắt quyết tử vì gia đình."
        },
        {
            "name": "Mô Hình Trafalgar D. Water Law Tuyệt Kỹ K-ROOM",
            "slug": "trafalgar-law-tuyet-ky-k-room",
            "category": cat_objs["that-vu-hai-sieu-tan-tinh"],
            "seller": seller_user,
            "price": 1150000,
            "original_price": 1400000,
            "height": "27 cm",
            "scale": "Tỷ lệ 1/8",
            "material": "PVC cao cấp",
            "brand": "Banpresto Vibration Stars",
            "weight": "880g",
            "is_featured": False,
            "in_stock": True,
            "image": "/static/hinh_anh/san_pham/law.png",
            "image_2": "https://images8.alphacoders.com/128/1288258.png",
            "image_3": "https://wallpapercave.com/wp/wp11894432.jpg",
            "image_4": "https://i.pinimg.com/736x/2c/3f/17/2c3f1737e968c991b15112ec7e584ec6.jpg",
            "description": "Bác sĩ tử thần Law với thanh Nodachi Kikoku được kéo dài xuyên thấu lòng đất Onigashima bằng năng lực Thức Tỉnh Ope Ope no Mi K-ROOM. Hiệu ứng sóng xung kích màu xanh lam sắc nét."
        },
        {
            "name": "Mô Hình Nữ Hoàng Hải Tặc Boa Hancock & Rắn Salome",
            "slug": "nu-hoang-hai-tac-boa-hancock-salome",
            "category": cat_objs["that-vu-hai-sieu-tan-tinh"],
            "seller": seller_user,
            "price": 1390000,
            "original_price": 1700000,
            "height": "29 cm",
            "scale": "Tỷ lệ 1/7",
            "material": "PVC cao cấp mạ bóng",
            "brand": "Megahouse P.O.P Ver.BB",
            "weight": "1100g",
            "is_featured": False,
            "in_stock": True,
            "image": "/static/hinh_anh/san_pham/boa_hancock.png",
            "image_2": "https://images2.alphacoders.com/133/1339178.png",
            "image_3": "https://wallpapercave.com/wp/wp12204899.jpg",
            "image_4": "https://i.pinimg.com/736x/01/be/19/01be199201940989f6645e9eebe756c7.jpg",
            "description": "Nữ Vương Đảo Amazon Lily Boa Hancock kiêu sa lộng lẫy ngồi trên chú rắn Salome trung thành. Nét mặt sắc sảo quyến rũ hóa đá mọi ánh nhìn cùng váy lụa xẻ tà tà thêu hoa văn hoa hồng tinh xảo."
        },
        {
            "name": "Mô Hình Mắt Diều Hâu Dracule Mihawk Đệ Nhất Kiếm",
            "slug": "dracule-mihawk-de-nhat-kiem-si",
            "category": cat_objs["that-vu-hai-sieu-tan-tinh"],
            "seller": seller_user,
            "price": 1550000,
            "original_price": 1900000,
            "height": "31 cm",
            "scale": "Tỷ lệ 1/7",
            "material": "PVC cao cấp",
            "brand": "Megahouse P.O.P NEO-MAXIMUM",
            "weight": "1300g",
            "is_featured": False,
            "in_stock": True,
            "image": "/static/hinh_anh/san_pham/mihawk.png",
            "image_2": "https://images7.alphacoders.com/132/1328406.png",
            "image_3": "https://wallpapercave.com/wp/wp11603527.jpg",
            "image_4": "https://i.pinimg.com/736x/6c/e2/0a/6ce20a6e03180fc1f31f90b9b3e15779.jpg",
            "description": "Kiếm sĩ mạnh nhất thế giới Dracule Mihawk cầm thanh Cực Phẩm Đại Bảo Kiếm Hắc Kiếm Yoru chém đứt tảng băng khổng lồ. Ánh mắt mắt diều hâu vàng sắc lạnh toát lên uy phong đỉnh cao kiếm đạo."
        },
        {
            "name": "Mô Hình Thủy Sư Đô Đốc Akainu Sakazuki Nham Thạch",
            "slug": "thuy-su-do-doc-akainu-sakazuki",
            "category": cat_objs["hai-quan-chinh-phu"],
            "seller": seller_user,
            "price": 1750000,
            "original_price": 2150000,
            "height": "32 cm",
            "scale": "Tỷ lệ 1/7",
            "material": "PVC & Resin nham thạch trong suốt",
            "brand": "Bandai Tamashii Nations",
            "weight": "1600g",
            "is_featured": False,
            "in_stock": True,
            "image": "/static/hinh_anh/san_pham/akainu.png",
            "image_2": "https://images3.alphacoders.com/132/1328407.png",
            "image_3": "https://wallpapercave.com/wp/wp11400275.jpg",
            "image_4": "https://i.pinimg.com/736x/9c/6e/88/9c6e885d58ff90299f1fae83fc918bc4.jpg",
            "description": "Thủy Sư Đô Đốc Sakazuki với nắm đấm Nham Thạch Đại Nham Cẩu sôi sục nhiệt độ nghìn độ C. Áo choàng Công Lý Hải Quân tung bay cùng nét mặt cương trực tuyệt đối không khoan nhượng với hải tặc."
        },
        {
            "name": "Mô Hình Anh Hùng Hải Quân Garp Galaxy Impact",
            "slug": "anh-hung-hai-quan-garp-galaxy-impact",
            "category": cat_objs["hai-quan-chinh-phu"],
            "seller": seller_user,
            "price": 2100000,
            "original_price": 2600000,
            "height": "33 cm",
            "scale": "Tỷ lệ 1/7",
            "material": "PVC & Resin Haki tia chớp đen",
            "brand": "Megahouse P.O.P",
            "weight": "1900g",
            "is_featured": True,
            "in_stock": True,
            "image": "/static/hinh_anh/san_pham/garp.png",
            "image_2": "https://images6.alphacoders.com/133/1339180.png",
            "image_3": "https://wallpapercave.com/wp/wp12204905.jpg",
            "image_4": "https://i.pinimg.com/736x/11/44/22/114422cb4244b706c646b9a89c894564.jpg",
            "description": "Trung Tướng Huyền Thoại Monkey D. Garp tung cú đấm Haki Bá Vương Tinh Cầu Bộc Phá (Galaxy Impact) nghiền nát Đảo Hải Tặc Hachinosu từ trên trời rơi xuống. Cú đấm kinh thiên động địa với hiệu ứng tia sét đen cực kỳ bùng nổ."
        },
        {
            "name": "Mô Hình Công Chúa Quỷ Yamato Raimei Hakke",
            "slug": "cong-chua-quy-yamato-raimei-hakke",
            "category": cat_objs["bang-mu-rom"],
            "seller": seller_user,
            "price": 1490000,
            "original_price": 1850000,
            "height": "29 cm",
            "scale": "Tỷ lệ 1/7",
            "material": "PVC cao cấp",
            "brand": "Bandai Ichiban Kuji",
            "weight": "1150g",
            "is_featured": False,
            "in_stock": True,
            "image": "/static/hinh_anh/san_pham/yamato.png",
            "image_2": "https://images7.alphacoders.com/129/1297127.png",
            "image_3": "https://wallpapercave.com/wp/wp11894436.jpg",
            "image_4": "https://i.pinimg.com/736x/d4/8a/7c/d48a7cb019ecfa05814578b871c8411c.jpg",
            "description": "Người con gái thừa kế ý chí của Oden - Yamato cầm cây chùy sắt Takeru chuẩn bị xuất chiêu Lôi Minh Bát Quái. Tóc ombre trắng xanh bồng bềnh cùng cặp sừng đỏ đặc trưng của tộc Quỷ hào khí ngút ngàn."
        },
        {
            "name": "Mô Hình Bác Sĩ Tony Tony Chopper Kung Fu Point",
            "slug": "bac-si-tony-tony-chopper-kungfu-point",
            "category": cat_objs["bang-mu-rom"],
            "seller": seller_user,
            "price": 490000,
            "original_price": 650000,
            "height": "16 cm",
            "scale": "Tỷ lệ 1/10",
            "material": "PVC đúc khối bền đẹp",
            "brand": "Banpresto Fluffy Puffy",
            "weight": "450g",
            "is_featured": False,
            "in_stock": True,
            "image": "/static/hinh_anh/san_pham/chopper.png",
            "image_2": "https://images5.alphacoders.com/133/1339179.png",
            "image_3": "https://wallpapercave.com/wp/wp11894437.jpg",
            "image_4": "https://i.pinimg.com/736x/c5/4b/32/c54b32f913d80bc0eb2a79ee5b190f82.jpg",
            "description": "Bác sĩ hải tặc đáng yêu nhất Đại Hải Trình Chopper trong tư thế Kung Fu Point tròn xoe hài hước nhưng cực kỳ nhanh nhẹn. Mũ hồng chữ thập trắng và chiếc mũi xanh độc nhất vô nhị."
        },
    ]

    for pdata in products_data:
        prod, created = Product.objects.update_or_create(
            slug=pdata["slug"],
            defaults=pdata
        )
        status = "✨ Tạo mới" if created else "🔄 Cập nhật"
        print(f" {status}: {prod.name} ({prod.price:,} đ) [Đã nạp 4 góc ảnh chi tiết]")

    print("\n🎉 HOÀN TẤT NẠP DỮ LIỆU MẪU MÔ HÌNH ONE PIECE SẮC NÉT!")


if __name__ == "__main__":
    run_seed()
