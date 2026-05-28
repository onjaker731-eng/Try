#!/bin/bash
# Простий скрипт для запуску YouTube Downloader

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Активуємо venv якщо він існує
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Запускаємо скрипт з аргументами
python ForTheDownloader.py "$@"
