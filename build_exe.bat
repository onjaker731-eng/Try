@echo off
REM Скрипт для створення .exe на Windows

echo.
echo ================================
echo YouTube Downloader - Build EXE
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
    echo Встановіть FFmpeg та додайте до PATH
    echo https://ffmpeg.org/download.html
    echo.
    echo Продовжуємо...
)
echo.

REM Створюємо venv
echo Створюю віртуальне середовище...
python -m venv venv
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Не вдалося активувати venv!
    pause
    exit /b 1
)
echo.

REM Встановлюємо залежності
echo Встановлюю залежності...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Не вдалося встановити залежності!
    pause
    exit /b 1
)
echo.

REM Встановлюємо PyInstaller
echo Встановлюю PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ERROR: Не вдалося встановити PyInstaller!
    pause
    exit /b 1
)
echo.

REM Компілюємо у .exe
echo Компіліюю у .exe файл...
echo Це може зайняти 1-2 хвилини...
pyinstaller --onefile --console --name "YouTube-Downloader" ForTheDownloader.py

if errorlevel 1 (
    echo ERROR: Не вдалося скомпілювати!
    pause
    exit /b 1
)
echo.

echo ================================
echo SUCCESS!
echo ================================
echo.
echo .exe файл знаходиться в папці: dist\
echo Запуск: dist\YouTube-Downloader.exe
echo.
pause
