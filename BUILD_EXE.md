# 📦 Як створити .exe файл

## ⚠️ Важливо!

PyInstaller **на Linux** створює Linux виконуваний файл (не Windows .exe).  
Щоб створити справжній **Windows .exe**, потрібна **Windows машина**.

## 🪟 Для Windows користувачів

### Метод 1: Використовувати готовий скрипт (найпростіше)

1. Завантажте всі файли на Windows
2. Відкрийте PowerShell або CMD в папці проекту
3. Запустіть:
```cmd
build_exe.bat
```

Скрипт автоматично:
- ✅ Перевірить Python
- ✅ Перевірить FFmpeg  
- ✅ Створить venv
- ✅ Встановить залежності
- ✅ Скомпілює .exe

### Метод 2: Вручну (більше контролю)

```cmd
# 1. Створити venv
python -m venv venv
call venv\Scripts\activate.bat

# 2. Встановити залежності
pip install -r requirements.txt

# 3. Встановити PyInstaller
pip install pyinstaller

# 4. Скомпілювати
pyinstaller --onefile --console --name "YouTube-Downloader" ForTheDownloader.py
```

### Метод 3: Розширена конфігурація

```cmd
# З іконкою та оптимізацією
pyinstaller --onefile ^
    --console ^
    --name "YouTube-Downloader" ^
    --distpath "./dist" ^
    --workpath "./build" ^
    --specpath "." ^
    --add-data "requirements.txt:." ^
    ForTheDownloader.py
```

## 📂 Результат

Після компіляції .exe буде в папці:
```
dist/
└── YouTube-Downloader.exe  (примерно 50-100 MB)
```

## ✅ Як використовувати .exe

### З командного рядка:
```cmd
dist\YouTube-Downloader.exe
```

### З параметрами:
```cmd
# Меню
dist\YouTube-Downloader.exe

# Для інших команд - використовуйте Python скрипт:
python ForTheDownloader.py --help
```

## 📊 Розміри файлів

| Файл | Розмір |
|------|--------|
| YouTube-Downloader.exe | 50-100 MB |
| Папка dist (з залежностями) | ~100-150 MB |

Великий розмір тому що:
- Python runtime включений
- yt-dlp з усіма залежностями
- FFmpeg біблієки (якщо включені)

## 🛠️ Оптимізація розміру

Якщо .exe занадто великий, можна:

### Варіант 1: Видалити непотрібні файли
```cmd
pyinstaller --onefile --console --strip ForTheDownloader.py
```

### Варіант 2: UPX компресія (якщо встановлено)
```cmd
# Встановити UPX:
# Windows: https://upx.github.io/

pyinstaller --onefile --console --upx-dir=C:\upx ForTheDownloader.py
```

### Варіант 3: Вибрати мінімум залежностей
```cmd
pyinstaller --onefile --console \
    --hidden-import=yt_dlp \
    ForTheDownloader.py
```

## 📱 Розповсюдження

Після компіляції можна:

1. **Залишити як одинарний .exe**
```
dist\YouTube-Downloader.exe
```

2. **Упакувати в ZIP**
```cmd
# Запакуйте папку dist/ у ZIP для розповсюдження
```

3. **Інстальник WinRAR/7-Zip**
```cmd
# Створіть SFX архів з .exe
```

## ⚠️ Потенційні проблеми

### Проблема: "FFmpeg not found"
**Рішення**: Встановіть FFmpeg на Windows:
```cmd
# Через Chocolatey:
choco install ffmpeg

# Або завантажте з:
# https://ffmpeg.org/download.html
```

### Проблема: Антивірус блокує .exe
**Рішення**: 
- Відключіть антивірус тимчасово
- Додайте папку в виключення
- Підпишіть .exe кодом

### Проблема: "can't find a usable init.py"
**Рішення**: 
```cmd
# Перевстановіть PyInstaller:
pip uninstall pyinstaller
pip install pyinstaller --upgrade
```

## 💡 Поради

- Завжди компілюйте на **тій ж версії Windows**, для якої призначено exe
- Тестуйте .exe перед розповсюдженням
- Включайте файл README в папці з .exe
- Розповідайте користувачам, що потрібен FFmpeg

## 📝 Структура для розповсюдження

```
YouTube-Downloader-v1.0/
├── YouTube-Downloader.exe
├── README.md
├── QUICKSTART.md
├── LICENSE
└── downloads/  (папка для файлів)
```

## 🔗 Корисні посилання

- [PyInstaller документація](https://pyinstaller.org/)
- [FFmpeg завантаження](https://ffmpeg.org/download.html)
- [UPX компресія](https://upx.github.io/)
- [Інсуноси для підписування .exe](https://docs.microsoft.com/en-us/windows-hardware/drivers/dashboard/code-signing-requirements)

---

**Версія**: 1.0  
**Останнє оновлення**: 2026  
**Платформи**: Windows (для .exe), Linux/macOS (Python скрипт)
