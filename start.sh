#!/bin/bash
# Script khởi động: migrate + seed + chạy server
echo "🔄 Đang chạy migrate..."
python manage.py migrate --noinput

echo "🌱 Đang seed dữ liệu..."
python seed_data.py

echo "🚀 Khởi động server Gunicorn..."
gunicorn du_an.wsgi:application --bind 0.0.0.0:8000
