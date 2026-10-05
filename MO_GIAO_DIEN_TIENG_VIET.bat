@echo off
chcp 65001 > nul
echo ==============================================================================
echo    🏴‍☠️ DANG MO DUA AN ONE PIECE STORE VOI GIAO DIEN TIENG VIET...
echo ==============================================================================
cd /d "%~dp0"
start "" code "OnePieceStore_TiengViet.code-workspace"
echo Da mo xong! Ban co the tat cua so nay.
timeout /t 3 > nul
exit
