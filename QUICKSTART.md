# 🚀 Швидка шпаргалка

## ⚡ Установка (один раз)

```bash
chmod +x install.sh
./install.sh
```

Або вручну:
```bash
python3 -m venv .venv
source .venv/bin/activate  # На Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 🎮 Запуск

### 1️⃣ Інтерактивне меню (найпростіше)
```bash
source .venv/bin/activate
python ForTheDownloader.py interactive
```

### 2️⃣ CLI команди

**Завантажити відео:**
```bash
python ForTheDownloader.py download "https://youtube.com/watch?v=..."
```

**Завантажити тільки звук:**
```bash
python ForTheDownloader.py download -a "https://youtube.com/watch?v=..."
```

**Отримати інформацію:**
```bash
python ForTheDownloader.py info "https://youtube.com/watch?v=..."
```

**В іншу папку:**
```bash
python ForTheDownloader.py -o ~/Videos download "https://..."
```

**Допомога:**
```bash
python ForTheDownloader.py --help
python ForTheDownloader.py download --help
```

### 3️⃣ Через run.sh (найзручніше на Linux)
```bash
chmod +x run.sh
./run.sh interactive
./run.sh download "URL"
./run.sh info "URL"
```

## 📊 Структура файлів

```
ForTheTry/
├── ForTheDownloader.py   # Основний скрипт
├── requirements.txt      # Залежності
├── README.md            # Повна документація
├── TIPS.md              # Поради та приклади
├── QUICKSTART.md        # ЦЕ ВИ ЗАРАЗ ЧИТАЄТЕ
├── install.sh           # Скрипт установки (Linux/macOS)
├── install.bat          # Скрипт установки (Windows)
├── run.sh               # Запуск скрипту (Linux/macOS)
└── downloads/           # Завантажені файли тут
```

## 💡 Поради

| Задача | Команда |
|--------|---------|
| Завантажити відео | `python ForTheDownloader.py download "URL"` |
| Завантажити аудіо | `python ForTheDownloader.py download -a "URL"` |
| Інформація | `python ForTheDownloader.py info "URL"` |
| Інтерактив | `python ForTheDownloader.py interactive` |
| Допомога | `python ForTheDownloader.py --help` |

## 🛠️ Вирішення проблем

| Помилка | Рішення |
|---------|---------|
| Модуль не знайдений | `source .venv/bin/activate` puis `pip install -r requirements.txt` |
| FFmpeg не знайдено | `sudo apt install ffmpeg` (Linux) або `brew install ffmpeg` (macOS) |
| Доступ заборонено | `chmod +x install.sh run.sh` |
| Відео не завантажується | Спробуйте: `pip install --upgrade yt-dlp` |

## 🌍 Приклади посилань

```
Звичайне відео:
https://www.youtube.com/watch?v=dQw4w9WgXcQ

YouTube Short:
https://www.youtube.com/shorts/7AQSdqKO6kc

Плейліст:
https://www.youtube.com/playlist?list=PLxxxxxx
```

---

**Для повної документації дивіться [README.md](README.md)**
