@echo off
cd /d "%~dp0"
py make_webp.py 2>nul || python make_webp.py
pause
