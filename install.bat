@echo off
REM Скрипт для установки всіх залежностей на Windows

echo.
echo ================================
echo YouTube Downloader Setup
echo ================================
echo.

REM Перевіряємо Python
echo Перевіряю Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python не встановлений!
    echo Завантажте з https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

REM Перевіряємо FFmpeg
echo Перевіряю FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: FFmpeg не встановлений!
    echo.
    echo Встановіть FFmpeg одним з методів:
    echo 1. Завантажте з https://ffmpeg.org/download.html
    echo 2. Або через Chocolatey: choco install ffmpeg
    echo 3. Або через Windows Package Manager: winget install ffmpeg
    echo.
    echo Продовжуємо...
)
echo.

REM Встановлюємо Python залежності
echo Встановлюю Python залежності...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Не вдалося встановити залежності!
    pause
    exit /b 1
)
echo.

echo ================================
echo Установка завершена!
echo ================================
echo.
echo Для запуску виконайте:
echo    python ForTheDownloader.py
echo.
pause
