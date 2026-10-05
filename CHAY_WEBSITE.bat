@echo off
chcp 65001 > nul
echo ==============================================================================
echo    🏴‍☠️ DANG KHOI DONG WEBSITE BAN MO HINH ONE PIECE STORE (DJANGO)
echo ==============================================================================
cd /d "%~dp0"
echo Web dang chay tai: http://127.0.0.1:8000/
start http://127.0.0.1:8000/
.\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
pause
