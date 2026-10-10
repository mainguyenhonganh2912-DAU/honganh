# ==============================================================================
# ⚙️ CẤU HÌNH ỨNG DỤNG CỬA HÀNG (cua_hang/apps.py)
# Khai báo cấu hình của app 'cua_hang' để Django nhận diện trong settings.py
# ==============================================================================
from django.apps import AppConfig


class CuaHangConfig(AppConfig):
    name = 'cua_hang'
    label = 'shops'
    verbose_name = 'Quản lý Cửa Hàng Mô Hình One Piece'
