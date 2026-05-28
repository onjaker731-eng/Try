#!/bin/bash
# Скрипт для установки всіх залежностей

echo "================================"
echo "🎬 YouTube Downloader Setup"
echo "================================"
echo ""

# Перевіряємо Python
echo "🔍 Перевіряю Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не встановлений!"
    exit 1
fi
echo "✅ Python3 знайдений"
python3 --version
echo ""

# Перевіряємо FFmpeg
echo "🔍 Перевіряю FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg не встановлений. Встановлюю..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y ffmpeg
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y ffmpeg
        elif command -v pacman &> /dev/null; then
            sudo pacman -S ffmpeg
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            brew install ffmpeg
        else
            echo "❌ Homebrew не встановлений. Встановіть його з https://brew.sh"
            exit 1
        fi
    fi
fi
echo "✅ FFmpeg знайдений"
ffmpeg -version | head -n 1
echo ""

# Створюємо venv
echo "📦 Створюю віртуальне середовище..."
python3 -m venv .venv
source .venv/bin/activate
echo "✅ Venv створено"
echo ""

# Встановлюємо Python залежності
echo "📦 Встановлюю Python залежності..."
pip install -r requirements.txt
echo "✅ Залежності встановлені"
echo ""

echo "================================"
echo "✅ Установка завершена!"
echo "================================"
echo ""
echo "🚀 Для запуску скрипту виконайте одну з команд:"
echo ""
echo "   # Активувати venv:"
echo "   source .venv/bin/activate"
echo ""
echo "   # Запустити програму:"
echo "   python ForTheDownloader.py --help"
echo "   python ForTheDownloader.py interactive"
echo ""
echo "   # Або використовуйте run.sh:"
echo "   chmod +x run.sh"
echo "   ./run.sh --help"
echo ""

