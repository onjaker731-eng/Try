[app]
# Назва і версія
title = YouTube Downloader
package.name = youtube_downloader
package.domain = com.vladix

# Версія
version = 1.0

# Вимоги
requirements = python3,kivy,yt-dlp,requests,certifi

# Файли додатку
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Дозволи Android
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

# Мінімальна версія Android
android.minapi = 21
android.targetapi = 31

# ABI архітектури
android.archs = arm64-v8a,armeabi-v7a

# Java версія
android.release_artifact = aab

# Гарячі кейс
android.hotspot = 1

# Дозволи на запис
android.permissions_request = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Режим fullscreen
fullscreen = 0

# Орієнтація
orientation = portrait

# Іконка (опціонально)
# icon.filename = %(source.dir)s/data/icon.png

# Приклад іконки
# icon.filename = %(source.dir)s/icon.png

# Екран завантаження
# presplash.filename = %(source.dir)s/presplash.png

# Точка входу
entrypoint = YouTubeDownloader_mobile

# Класи для включення
p4a.branch = develop
p4a.bootstrap = sdl2
p4a.arch = arm64-v8a

# Будівництво
log_level = 2
warn_on_root = 1
