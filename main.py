#!/usr/bin/env python3
"""
YouTube Video & Shorts Downloader
Професійний та чистий скрипт для завантаження контенту з YouTube.
"""

import sys
from datetime import datetime
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("❌ Модуль yt-dlp не встановлений.")
    print("Встановіть його командою: pip install yt-dlp")
    sys.exit(1)

# Виносимо конфігурацію окремо (Позбавляємось хардкоду)
DEFAULT_DOWNLOAD_DIR = "downloads"
FFMPEG_AUDIO_OPTS = {
    "key": "FFmpegExtractAudio",
    "preferredcodec": "mp3",
    "preferredquality": "192",
}


class YouTubeDownloader:
    def __init__(self, output_dir: str = DEFAULT_DOWNLOAD_DIR):
        # Використовуємо modern pathlib замість os.path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Шаблон збереження файлів
        self.out_template = str(self.output_dir / "%(title)s.%(ext)s")

    def get_video_info(self, url: str) -> dict | None:
        """Отримує детальну інформацію про відео."""
        ydl_opts = {"quiet": True, "no_warnings": True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    return None
                
                return {
                    "title": info.get("title", "Unknown"),
                    "duration": info.get("duration", 0),
                    "uploader": info.get("uploader", "Unknown"),
                    "formats_available": len(info.get("formats", [])),
                }
        except Exception:
            return None

    def print_video_info(self, info: dict) -> None:
        """Виводить інформацію про відео в консоль (Усуваємо дублювання коду - DRY)."""
        minutes, seconds = divmod(info["duration"], 60)
        print(f"\n📹 Назва: {info['title']}")
        print(f"⏱️ Тривалість: {minutes}:{seconds:02d}")
        print(f"👤 Канал: {info['uploader']}")
        print(f"📊 Доступних форматів: {info['formats_available']}")

    def download_video(self, url: str, audio_only: bool = False) -> bool:
        """Завантажує відео або аудіо в найвищій якості."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n🎬 [{timestamp}] Початок завантаження...")
        print(f"📍 URL: {url}")

        info = self.get_video_info(url)
        if not info:
            print("❌ Не вдалося отримати інформацію про відео. Перевірте посилання.")
            return False

        self.print_video_info(info)

        # Динамічно формуємо конфігурацію для yt_dlp
        ydl_opts = {
            "outtmpl": self.out_template,
            "quiet": False,
            "no_warnings": False,
            "progress_hooks": [self.progress_hook],
        }

        if audio_only:
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [FFMPEG_AUDIO_OPTS],
            })
            print("🔊 Режим: тільки аудіо (MP3)")
        else:
            ydl_opts.update({
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
                "postprocessors": [{
                    "key": "FFmpegConcat",
                    "only_multi_video": False,
                    "when": "playlist",
                }],
            })
            print("🎥 Режим: відео + аудіо (найвища якість)")

        try:
            print("\n⏳ Завантаження розпочато...\n")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                download_info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(download_info)
                print(f"\n✅ Завантаження успішне!")
                print(f"💾 Файл збережено: {filename}")
                return True
        except Exception as e:
            print(f"\n❌ Помилка при завантаженні: {e}")
            return False

    def progress_hook(self, d: dict) -> None:
        """Відображає прогрес завантаження в одному рядку."""
        status = d.get("status")
        if status == "downloading":
            percent = d.get("_percent_str", "N/A")
            speed = d.get("_speed_str", "N/A")
            eta = d.get("_eta_str", "N/A")
            print(f"📥 {percent} | Швидкість: {speed} | Залишилось: {eta}", end="\r")
        elif status == "finished":
            print("\n✓ Завантаження завершено, обробка файлу...", end="\r")


def show_menu() -> None:
    print(f"\n{'-' * 60}")
    print(" 🎬 YouTube Video Downloader (Middle Version) ")
    print(f"{'-' * 60}")
    print(" 1️⃣ Завантажити відео в найвищій якості ")
    print(" 2️⃣ Завантажити тільки аудіо (MP3) ")
    print(" 3️⃣ Дізнатись інформацію про відео ")
    print(" 4️⃣ Вихід ")
    print(f"{'-' * 60}")


def main() -> None:
    downloader = YouTubeDownloader()
    
    # Використовуємо словник для мапінгу дій замість громіздких if/elif
    actions = {
        "1": lambda url: downloader.download_video(url, audio_only=False),
        "2": lambda url: downloader.download_video(url, audio_only=True),
    }

    while True:
        show_menu()
        choice = input("\n👉 Виберіть опцію (1-4): ").strip()

        if choice == "4":
            print("👋 До побачення!")
            break

        if choice not in ["1", "2", "3"]:
            print("❌ Невірний вибір. Спробуйте ще раз.")
            continue

        url = input("\n🔗 Введіть посилання на YouTube відео: ").strip()
        if not url:
            print("❌ Посилання не введено.")
            continue

        if choice in actions:
            actions[choice](url)
        elif choice == "3":
            info = downloader.get_video_info(url)
            if info:
                downloader.print_video_info(info)
            else:
                print("❌ Не вдалося отримати інформацію про відео.")

        input("\n👉 Натисніть Enter для продовження...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Скрипт перервано користувачем.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Критична помилка: {e}")
        sys.exit(1)
