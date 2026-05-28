# 🎬 YouTube Video Downloader

Потужний професійний скрипт для завантаження відео з YouTube та YouTube Shorts в найвищій якості.

**Написаний з використанням:**
- ✅ `Click` - для професійного CLI інтерфейсу
- ✅ `yt-dlp` - для завантаження відео
- ✅ `FFmpeg` - для обробки медіафайлів

## 📋 Можливості

- ✅ Завантаження відео в найвищій якості (H.264, 4K якщо доступна)
- ✅ Автоматичне об'єднання відео та аудіо
- ✅ Завантаження тільки аудіо (MP3 формат)
- ✅ Підтримка YouTube Shorts
- ✅ Показ прогресу завантаження
- ✅ Інформація про відео (тривалість, канал, тощо)
- ✅ **Професійний CLI інтерфейс** з командами
- ✅ Інтерактивний режим для зручного використання
- ✅ Кольоровий вивід з іконками

## 🚀 Установка

### Крок 1: Встановлення Python залежностей

```bash
pip install -r requirements.txt
```

### Крок 2: Встановлення FFmpeg (ВАЖЛИВО!)

FFmpeg необхідний для об'єднання відео та аудіо.

#### На Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

#### На Linux (Fedora):
```bash
sudo dnf install ffmpeg
```

#### На macOS:
```bash
brew install ffmpeg
```

#### На Windows:
Завантажте з https://ffmpeg.org/download.html або використовуйте:
```bash
choco install ffmpeg
```

### Крок 3: Перевірка установки

```bash
ffmpeg -version
python -m pip install -r requirements.txt
```

## 📖 Використання

### Запуск з CLI командами:

```bash
# Перегляд всіх команд
python ForTheDownloader.py --help

# Завантажити відео
python ForTheDownloader.py download "https://www.youtube.com/watch?v=..."

# Завантажити тільки аудіо
python ForTheDownloader.py download -a "https://www.youtube.com/watch?v=..."

# Отримати інформацію про відео
python ForTheDownloader.py info "https://www.youtube.com/watch?v=..."

# Вказати папку для завантажень
python ForTheDownloader.py -o /path/to/folder download "https://www.youtube.com/watch?v=..."

# Запустити інтерактивний режим з меню
python ForTheDownloader.py interactive
```

### Інтерактивний режим (меню):

```bash
python ForTheDownloader.py interactive
```

Запустить красиве меню з опціями для вибору.

### CLI Опції:

```
--help, -h          Показати довідку
--output, -o PATH   Папка для завантажень (за замовчуванням: downloads)
```

### Команди:

| Команда | Опис |
|---------|------|
| `download` | Завантажити відео |
| `info` | Отримати інформацію про відео |
| `interactive` | Запустити інтерактивний режим |
| `version` | Показати версію |

## 💾 Де знаходяться завантажені файли?

Всі файли зберігаються в папці `downloads/` (або в вказаній папці через `-o`).

```bash
# Завантажити в конкретну папку
python ForTheDownloader.py -o ~/Videos download "https://..."
```

## 🔍 Форматизація файлів

- **Відео**: MP4 (найвища доступна якість)
- **Аудіо**: MP3 320 kbps

## 📚 Приклади

### Приклад 1: Завантажити звичайне відео
```bash
python ForTheDownloader.py download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Приклад 2: Завантажити YouTube Short
```bash
python ForTheDownloader.py download "https://www.youtube.com/shorts/7AQSdqKO6kc"
```

### Приклад 3: Завантажити тільки звук
```bash
python ForTheDownloader.py download -a "https://www.youtube.com/watch?v=..."
```

### Приклад 4: Перевірити інформацію про відео
```bash
python ForTheDownloader.py info "https://www.youtube.com/watch?v=..."
```

### Приклад 5: Завантажити в конкретну папку
```bash
python ForTheDownloader.py -o ~/Music download -a "https://..."
```

### Приклад 6: Інтерактивний режим
```bash
python ForTheDownloader.py interactive
```

## ⚙️ Розширені опції (для просунутих користувачів)

Якщо потрібні додаткові параметри, можна редагувати `ydl_opts` у функції `download_video()`.

### Популярні формати:

```
'best' - найкраща комбінація
'bestvideo+bestaudio' - найкраще відео + найкраще аудіо
'worstvideo+worstaudio' - найгірша якість (найменший розмір)
```

## ⚠️ Важливо!

- **Авторські права**: Завантажуйте тільки вміст, на який у вас є права або який дозволено завантажувати
- **Умови обслуговування**: Переконайтесь, що використання відповідає умовам YouTube
- **Локальна копія**: Завантажені файли - це локальні копії для вашого особистого використання

## 🐛 Розв'язання проблем

### Помилка: "No module named 'click'" або "No module named 'yt_dlp'"
```bash
pip install -r requirements.txt --upgrade
```

### Помилка: "FFmpeg not found"
Встановіть FFmpeg за інструкціями вище

### Повільне завантаження
- Перевірте швидкість інтернету
- Спробуйте завантажити в нижчій якості (редагуйте формат в коді)

### Відео не завантажується
- Перевірте коректність посилання
- Переконайтесь, що відео доступне у вашій країні
- Спробуйте обновити `yt-dlp`: `pip install yt-dlp --upgrade`

## 📝 Логи

Повні логи завантаження будуть показані в консолі з інформацією про:
- Швидкість завантаження
- Час, що залишився
- Розмір файлу
- Статус обробки

## 🔗 Корисні посилання

- [Click документація](https://click.palletsprojects.com/)
- [yt-dlp документація](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg документація](https://ffmpeg.org/)

---

**Версія**: 1.1  
**Останнє оновлення**: 2026  
**Архітектура**: CLI з Click  
**Ліцензія**: MIT
