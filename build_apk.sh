#!/bin/bash
# Скрипт для компіляції APK на Linux

echo "================================"
echo "📱 YouTube Downloader APK Build"
echo "================================"
echo ""

# Перевірка Python
echo "🔍 Перевіряю Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не встановлений!"
    exit 1
fi
python3 --version
echo ""

# Перевірка Java
echo "🔍 Перевіряю Java..."
if ! command -v java &> /dev/null; then
    echo "❌ Java не встановлений!"
    echo "Встановіть: sudo apt-get install openjdk-11-jdk"
    exit 1
fi
java -version
echo ""

# Перевірка Android SDK
echo "🔍 Перевіряю Android SDK..."
if [ -z "$ANDROID_SDK_ROOT" ]; then
    echo "⚠️  ANDROID_SDK_ROOT не встановлено"
    echo "Встановіть змінну середовища ANDROID_SDK_ROOT"
    echo "Приклад: export ANDROID_SDK_ROOT=\$HOME/Android"
    exit 1
fi
echo "✅ Android SDK: $ANDROID_SDK_ROOT"
echo ""

# Встановлення Buildozer та залежностей
echo "📦 Встановлюю Buildozer..."
pip install buildozer
pip install Cython==0.29.30
pip install kivy
echo ""

# Компіляція
echo "🚀 Компіляція APK (це може займти 10-30 хвилин)..."
echo ""

if [ "$1" == "release" ]; then
    buildozer android release
    APK_FILE=$(ls -t bin/*.apk 2>/dev/null | head -1)
    echo ""
    echo "✅ Release APK створено: $APK_FILE"
else
    buildozer android debug
    APK_FILE=$(ls -t bin/*.apk 2>/dev/null | head -1)
    echo ""
    echo "✅ Debug APK створено: $APK_FILE"
fi

echo ""
echo "================================"
echo "✅ Завершено!"
echo "================================"
echo ""
echo "APK файл: $APK_FILE"
echo ""
echo "Для встановлення на пристрій:"
echo "  adb install $APK_FILE"
echo ""
