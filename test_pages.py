import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'du_an.settings')
django.setup()

from django.test import Client

tests = [
    ('Trang chu', '/'),
    ('Dang nhap', '/dang-nhap/'),
    ('Dang ky', '/dang-ky/'),
    ('Gio hang', '/gio-hang/'),
    ('Chi tiet SP 1', '/san-pham/1/'),
]

print('=== TEST CAC TRANG ===')
c = Client()
for name, url in tests:
    try:
        resp = c.get(url, follow=True)
        icon = 'OK  ' if resp.status_code == 200 else 'FAIL'
        print(f'[{icon}] {name} ({url}) => {resp.status_code}')
    except Exception as e:
        print(f'[ERR ] {name} ({url}) => {e}')

# Test buyer login
c2 = Client()
c2.post('/dang-nhap/', {'username': 'nguoimua', 'password': 'buyer123'})
resp = c2.get('/thanh-toan/', follow=True)
icon = 'OK  ' if resp.status_code == 200 else 'FAIL'
print(f'[{icon}] Thanh toan (buyer login) => {resp.status_code}')

# Test seller
c3 = Client()
c3.post('/dang-nhap/', {'username': 'nguoiban', 'password': 'seller123'})
resp = c3.get('/kenh-nguoi-ban/', follow=True)
icon = 'OK  ' if resp.status_code == 200 else 'FAIL'
print(f'[{icon}] Kenh nguoi ban => {resp.status_code}')

resp = c3.get('/kenh-nguoi-ban/san-pham/them/', follow=True)
icon = 'OK  ' if resp.status_code == 200 else 'FAIL'
print(f'[{icon}] Form them san pham (4 anh) => {resp.status_code}')

# Test admin
c4 = Client()
c4.post('/dang-nhap/', {'username': 'admin', 'password': 'admin123'})
resp = c4.get('/quan-tri/', follow=True)
icon = 'OK  ' if resp.status_code == 200 else 'FAIL'
print(f'[{icon}] Cong quan tri => {resp.status_code}')

resp = c4.get('/quan-tri/san-pham/', follow=True)
icon = 'OK  ' if resp.status_code == 200 else 'FAIL'
print(f'[{icon}] Admin - Quan ly san pham => {resp.status_code}')

resp = c4.get('/quan-tri/nguoi-dung/', follow=True)
icon = 'OK  ' if resp.status_code == 200 else 'FAIL'
print(f'[{icon}] Admin - Quan ly nguoi dung => {resp.status_code}')

print()
print('=== DATABASE ===')
from cua_hang.models import Product, Order, UserProfile
print(f'  San pham: {Product.objects.count()}')
print(f'  Don hang: {Order.objects.count()}')
print(f'  Tai khoan: {UserProfile.objects.count()}')
p = Product.objects.filter(image_2__isnull=False).first()
if p:
    name_short = p.name[:40] if p.name else '(no name)'
    print(f'  SP co 4 anh: {name_short}')
    print(f'    image_2: {str(p.image_2)[:70]}')
else:
    print('  Chua co SP nao co image_2 - can chay seed_data.py lai')
print()
print('=== XONG ===')
