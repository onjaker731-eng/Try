# 💡 Поради та Приклади

## 🚀 Швидкий старт

### Для всіх ОС:
```bash
# 1. Встановити залежності
pip install -r requirements.txt

# 2. Запустити програму
python ForTheDownloader.py --help
```

## 📚 Приклади команд

### CLI команди

#### 1. Базовий завантаж
```bash
python ForTheDownloader.py download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

#### 2. Завантажити тільки аудіо
```bash
python ForTheDownloader.py download -a "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

#### 3. Вказати папку для завантажень
```bash
python ForTheDownloader.py -o ~/Videos download "https://www.youtube.com/watch?v=..."
```

#### 4. Отримати інформацію про відео
```bash
python ForTheDownloader.py info "https://www.youtube.com/watch?v=..."
```

#### 5. Запустити інтерактивне меню
```bash
python ForTheDownloader.py interactive
```

#### 6. Переглянути всі команди
```bash
python ForTheDownloader.py --help
```

### Інтерактивний режим
1. Запустити: `python ForTheDownloader.py interactive`
2. Вибрати опцію з меню
3. Вставити посилання
4. Чекати завантаження ✅

## 🎯 Лайфхаки

### Завантаження плейліста
```bash
python ForTheDownloader.py download "https://www.youtube.com/playlist?list=PLxxxxxx"
```

### Як отримати посилання?
1. Відкрийте відео на YouTube
2. Натисніть "Поділитись"
3. Скопіюйте посилання
4. Вставте в командний рядок

### Де знайти мої файли?
- Стандартно: папка `downloads/` поруч зі скриптом
- Або в папці, яку ви вказали через `-o`

### Завантажити у папку за запитом
```bash
# Напишіть алієс в .bashrc або .zshrc
alias youtube-dl="python3 /path/to/ForTheDownloader.py download"

# Потім просто:
youtube-dl "https://..."
```

### Обробити кілька відео
```bash
#!/bin/bash
# Збережіть як batch_download.sh

urls=(
    "https://youtube.com/watch?v=ID1"
    "https://youtube.com/watch?v=ID2"
    "https://youtube.com/watch?v=ID3"
)

for url in "${urls[@]}"; do
    python ForTheDownloader.py download "$url"
done
```

## 🛠️ Розв'язання поширених проблем

| Проблема | Рішення |
|----------|--------|
| "ModuleNotFoundError: No module named 'click'" | `pip install -r requirements.txt --upgrade` |
| "No module named 'yt_dlp'" | `pip install yt-dlp --upgrade` |
| "FFmpeg not found" | Встановіть FFmpeg за інструкціями |
| "This video is not available in your country" | Використовуйте VPN |
| "Video unavailable" | Відео видалено або приватне |
| Повільне завантаження | Перевірте швидкість інтернету |
| "Permission denied" на Linux | `chmod +x *.sh` |
| "Click command not found" | Встановіть: `pip install click` |

## 📊 Якість видео

| Якість | Формат | Розмір (на хв) |
|--------|--------|----------------|
| 4K (2160p) | MP4 (VP9/H.264) | 100-200 MB |
| 1080p | MP4 (H.264) | 30-50 MB |
| 720p | MP4 (H.264) | 15-30 MB |
| 360p | MP4 (H.264) | 5-10 MB |

## 🔐 Безпека та конфіденційність

- Скрипт не передає ніякі дані в інтернет
- Всі операції виконуються локально на вашому комп'ютері
- Завантажені файли зберігаються тільки на вашому диску
- Немає трекування або логування дій

## 💻 Команди для розробників

### Перевірити синтаксис
```bash
python -m py_compile ForTheDownloader.py
```

### Запустити з verbose
```bash
python -u ForTheDownloader.py download "URL" 2>&1 | tee download.log
```

### Отримати допомогу по конкретній команді
```bash
python ForTheDownloader.py download --help
python ForTheDownloader.py info --help
python ForTheDownloader.py interactive --help
```

## 🎨 Кольорові команди (Click особливості)

Click автоматично забарвлює вивід:
- 🔴 Червоний - помилки (`fg='red'`)
- 🟢 Зелений - успіх (`fg='green'`)
- 🔵 Синій - інформація (`fg='blue'`)
- 🟦 Блакитний - основні дані (`fg='cyan'`)
- 🟨 Жовтий - попередження (`fg='yellow'`)

## 📞 Підтримка

Якщо виникли проблеми:
1. Перевірте, що Python 3.7+ встановлений
2. Встановіть залежності: `pip install -r requirements.txt`
3. Перевірте, що FFmpeg встановлений
4. Оновіть бібліотеки: `pip install --upgrade -r requirements.txt`
5. Перевірте посилання на відео

## 📄 Ліцензійна інформація

Цей скрипт використовує:
- **Click**: BSD License
- **yt-dlp**: Публічна ліцензія (Unlicense)
- **FFmpeg**: LGPL

Програма надається "як є" без будь-яких гарантій.

---

**Версія**: 1.1  
**Останнє оновлення**: 2026  
**Архітектура**: CLI-based з Click  
**Гарантовано працює з**: Python 3.7+
