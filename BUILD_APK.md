# 📱 Як створити APK файл для Android

## ⚠️ Важливо!

Для компіляції APK потрібна **Linux машина** або **Windows WSL2** з Java SDK та Android SDK.

**На macOS та Windows без WSL2** це буде складніше.

---

## 📋 Системні вимоги

### Linux (Ubuntu/Debian) - РЕКОМЕНДУЄТЬСЯ

```bash
# 1. Python 3.8+
python3 --version

# 2. Java Development Kit (JDK)
sudo apt-get install openjdk-11-jdk

# 3. Android SDK
# Завантажте Android Studio або використайте command-line tools
# https://developer.android.com/studio

# 4. Buildozer та залежності
pip install buildozer
pip install Cython==0.29.30
```

### Для Windows (WSL2)

```bash
# Встановіть WSL2
# Потім всередині WSL встановіть усе як для Linux
```

### На macOS

Не рекомендується без Homebrew. Складніше, ніж на Linux.

---

## 🚀 Компіляція APK на Linux

### Крок 1: Встановлення залежностей

```bash
cd /home/vladisx/ForTheTry

# Встановіть Buildozer та Cython
pip install buildozer
pip install Cython==0.29.30
pip install kivy
```

### Крок 2: Встановлення Android SDK

Два способи:

#### Способ А: Android Studio (графічний інтерфейс)
1. Завантажте: https://developer.android.com/studio
2. Встановіть Android SDK
3. Нотуйте шляхи в PATH

#### Способ Б: Command-line tools (автоматичний)
```bash
# Завантажте
cd ~/Android
wget https://dl.google.com/android/repository/commandlinetools-linux-*.zip
unzip commandlinetools-linux-*.zip
mv cmdline-tools latest
mkdir -p cmdline-tools
mv latest cmdline-tools/

# Додайте в PATH (~/.bashrc або ~/.zshrc)
export ANDROID_SDK_ROOT=~/Android
export PATH=$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin
export PATH=$PATH:$ANDROID_SDK_ROOT/platform-tools

source ~/.bashrc  # або ~/.zshrc
```

### Крок 3: Встановлення компонентів Android

```bash
# Приймаємо ліцензії
sdkmanager --licenses

# Встановлюємо компоненти
sdkmanager "platform-tools"
sdkmanager "platforms;android-31"
sdkmanager "ndk;23.1.7779620"
sdkmanager "build-tools;31.0.0"
```

### Крок 4: Встановлення Java

```bash
# Перевірте Java
java -version
javac -version

# Якщо не встановлено
sudo apt-get install openjdk-11-jdk

# Встановіть JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

### Крок 5: Встановлення Buildozer

```bash
pip install buildozer
```

### Крок 6: Компіляція

```bash
cd /home/vladisx/ForTheTry

# Перша компіляція (установка всього)
buildozer android debug

# або для релізу
buildozer android release
```

Це займе **10-30 хвилин** при першій компіляції.

### Крок 7: APK файл

APK буде в папці:
```
bin/youtube_downloader-1.0-debug.apk
```

---

## 🎯 Результат

Після успішної компіляції:
```
bin/
├── youtube_downloader-1.0-debug.apk    # Для тестування
└── youtube_downloader-1.0-release.apk  # Для Google Play (опціонально)
```

---

## 📱 Встановлення на Android пристрій

### Варіант 1: USB з комп'ютера

```bash
# Підключіть Android пристрій USB кабелем
# Увімкніть режим розробника (Settings > About Phone > tap Build Number 7 times)

# Встановіть APK
adb install bin/youtube_downloader-1.0-debug.apk
```

### Варіант 2: Передача файлу

1. Скопіюйте .apk файл на USB накопичувач
2. Перейшліть на Android пристрій
3. Відкрийте файл менеджер
4. Натисніть на .apk файл для встановлення

### Варіант 3: Розповсюдження

Завантажте на Google Play для всіх користувачів.

---

## 🛠️ Розв'язання проблем

### Помилка: "android-sdk not found"
```bash
export ANDROID_SDK_ROOT=~/Android
export PATH=$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin
```

### Помилка: "java not found"
```bash
sudo apt-get install openjdk-11-jdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

### Помилка: "Gradle build failed"
```bash
# Видаліть кеш
rm -rf .buildozer/

# Спробуйте знов
buildozer android debug
```

### Помилка: "yt-dlp not available"
```bash
# Додайте в buildozer.spec
requirements = python3,kivy,yt-dlp,requests,certifi
```

### Повільна компіляція
Це нормально! Перша компіляція займає 15-30 хвилин.

---

## 📊 Розміри файлів

| Тип | Розмір |
|-----|--------|
| debug.apk | 50-100 MB |
| release.apk | 40-80 MB |

Велики розмір тому що:
- Python runtime
- Kivy framework
- yt-dlp та залежності
- Android bilabiotheken

---

## 🔧 Налаштування (buildozer.spec)

### Іконка
```ini
icon.filename = %(source.dir)s/icon.png
```

### Екран завантаження
```ini
presplash.filename = %(source.dir)s/presplash.png
```

### Назва пакету
```ini
package.name = youtube_downloader
package.domain = com.vladix
title = YouTube Downloader
```

### Дозволи Android
```ini
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
```

---

## 📝 Швидкий довідник

| Задача | Команда |
|--------|---------|
| Побудова debug | `buildozer android debug` |
| Побудова release | `buildozer android release` |
| Встановлення на пристрій | `adb install bin/*.apk` |
| Чистка кешу | `rm -rf .buildozer/` |
| Переглянути логи | `buildozer android logcat` |

---

## 🔗 Корисні посилання

- [Buildozer документація](https://buildozer.readthedocs.io/)
- [Kivy документація](https://kivy.org/docs/guide/basic.html)
- [Android SDK](https://developer.android.com/studio)
- [ADB Commands](https://developer.android.com/studio/command-line/adb)

---

## ✅ Контрольний список

- [ ] Python 3.8+ встановлено
- [ ] Java JDK встановлено
- [ ] Android SDK встановлено
- [ ] Buildozer встановлено
- [ ] buildozer.spec налаштовано
- [ ] YouTubeDownloader_mobile.py готовий
- [ ] Побудова завершена
- [ ] APK встановлено на пристрій
- [ ] Тестування завершено

---

**Версія**: 1.0  
**Платформа**: Android 5.0+  
**Мова**: Python 3.8+  
**Framework**: Kivy + Buildozer
