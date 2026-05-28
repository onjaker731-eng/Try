#!/usr/bin/env python3
"""
YouTube Video Downloader
Завантажує відео з YouTube та YouTube Shorts в найвищій якості
"""

import os
import sys
from pathlib import Path
from datetime import datetime

try:
    import click
    import yt_dlp
except ImportError as e:
    missing = str(e).split("'")[1]
    print(f"❌ Модуль {missing} не встановлений.")
    print(f"Встановіть його командою: pip install {missing}")
    sys.exit(1)


class YouTubeDownloader:
    def __init__(self, output_dir="downloads"):
        """Ініціалізація завантажувача"""
        self.output_dir = output_dir
        self.create_output_dir()
        
    def create_output_dir(self):
        """Створення папки для завантажень"""
        Path(self.output_dir).mkdir(exist_ok=True)
        
    def get_video_info(self, url):
        """Отримання інформації про відео"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'formats_available': len(info.get('formats', [])),
                }
        except Exception as e:
            return None
            
    def download_video(self, url, audio_only=False, quality='best'):
        """
        Завантаження відео в найвищій якості
        
        Args:
            url: посилання на YouTube відео або Short
            audio_only: Якщо True, завантажує тільки аудіо
            quality: Якість відео ('best', '720p', '1080p', '4k')
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        click.echo(f"\n🎬 [{timestamp}] Початок завантаження...")
        click.echo(f"📍 URL: {url}")
        
        # Отримання інформації про відео
        info = self.get_video_info(url)
        if not info:
            click.echo("❌ Не вдалося отримати інформацію про відео. Перевірте посилання.")
            return False
            
        click.echo(f"📹 Назва: {info['title']}")
        click.echo(f"⏱️  Тривалість: {info['duration']//60}:{info['duration']%60:02d}")
        click.echo(f"👤 Канал: {info['uploader']}")
        click.echo(f"📊 Доступних форматів: {info['formats_available']}")
        
        # Параметри завантаження
        if audio_only:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
                'progress_hooks': [self.progress_hook],
            }
            click.echo("🔊 Режим: тільки аудіо (MP3)")
        else:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegConcat',
                    'only_multi_video': False,
                    'when': 'playlist',
                }],
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
                'progress_hooks': [self.progress_hook],
            }
            click.echo("🎥 Режим: відео + аудіо (найвища якість)")
        
        try:
            click.echo("\n⏳ Завантаження розпочато...\n")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
            click.echo(f"\n✅ Завантаження успішне!")
            click.secho(f"💾 Файл збережено: {filename}", fg='green', bold=True)
            return True
            
        except Exception as e:
            click.echo(f"\n❌ Помилка при завантаженні: {str(e)}")
            return False
    
    def progress_hook(self, d):
        """Показ прогресу завантаження"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            click.echo(f"📥 {percent} | Швидкість: {speed} | Залишилось: {eta}", nl=False)
        elif d['status'] == 'finished':
            click.echo(f"\n✓ Завантаження завершено, обробка файлу...", nl=False)

# Глобальна змінна для завантажувача
downloader = None


@click.group()
@click.option(
    '--output', '-o',
    type=click.Path(),
    default='downloads',
    help='Папка для завантажень (за замовчуванням: downloads)'
)
@click.pass_context
def cli(ctx, output):
    """
    🎬 YouTube Video Downloader
    
    Завантажуй відео з YouTube та YouTube Shorts в найвищій якості
    """
    global downloader
    downloader = YouTubeDownloader(output_dir=output)
    ctx.ensure_object(dict)
    ctx.obj['downloader'] = downloader


@cli.command()
@click.argument('url')
@click.option(
    '--audio-only', '-a',
    is_flag=True,
    help='Завантажити тільки аудіо (MP3)'
)
@click.pass_context
def download(ctx, url, audio_only):
    """
    📥 Завантажити відео з YouTube
    
    URL: посилання на YouTube відео або Short
    
    Приклади:
    \b
    yt-downloader download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    yt-downloader download -a "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    """
    downloader = ctx.obj['downloader']
    try:
        success = downloader.download_video(url, audio_only=audio_only)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        click.echo("\n\n⏹️  Завантаження перервано користувачем.")
        sys.exit(0)
    except Exception as e:
        click.secho(f"❌ Критична помилка: {str(e)}", fg='red')
        sys.exit(1)


@cli.command()
@click.argument('url')
@click.pass_context
def info(ctx, url):
    """
    ℹ️  Отримати інформацію про відео
    
    URL: посилання на YouTube відео
    
    Показує: назву, тривалість, канал, кількість форматів
    
    Приклад:
    \b
    yt-downloader info "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    """
    downloader = ctx.obj['downloader']
    try:
        click.echo(f"\n🔍 Отримую інформацію про видео...\n")
        info = downloader.get_video_info(url)
        
        if not info:
            click.secho("❌ Не вдалося отримати інформацію про відео.", fg='red')
            sys.exit(1)
        
        click.secho(f"📹 Назва: {info['title']}", fg='cyan')
        click.secho(f"⏱️  Тривалість: {info['duration']//60}:{info['duration']%60:02d}", fg='cyan')
        click.secho(f"👤 Канал: {info['uploader']}", fg='cyan')
        click.secho(f"📊 Доступних форматів: {info['formats_available']}", fg='cyan')
        click.echo()
        
    except Exception as e:
        click.secho(f"❌ Помилка: {str(e)}", fg='red')
        sys.exit(1)


@cli.command()
def version():
    """
    📌 Показати версію програми
    """
    click.echo("YouTube Video Downloader v1.0")
    click.echo("Використовує: yt-dlp + FFmpeg")


@cli.command()
def interactive():
    """
    🎮 Запустити інтерактивний режим
    
    Меню з можливістю вибору операцій
    """
    downloader = None
    
    while True:
        click.clear()
        click.secho("=" * 60, fg='blue', bold=True)
        click.secho("🎬 YouTube Video Downloader", fg='cyan', bold=True)
        click.secho("=" * 60, fg='blue', bold=True)
        click.echo("1️⃣  Завантажити відео (відео + аудіо)")
        click.echo("2️⃣  Завантажити тільки аудіо (MP3)")
        click.echo("3️⃣  Отримати інформацію про відео")
        click.echo("4️⃣  Змінити папку для завантажень")
        click.echo("5️⃣  Вихід")
        click.secho("=" * 60, fg='blue', bold=True)
        
        choice = click.prompt("👉 Виберіть опцію", type=click.Choice(['1', '2', '3', '4', '5']))
        
        if choice == '5':
            click.secho("👋 До побачення!", fg='green')
            break
        
        if choice == '4':
            new_dir = click.prompt("📂 Введіть нову папку для завантажень", type=click.Path())
            downloader = YouTubeDownloader(output_dir=new_dir)
            click.secho(f"✅ Папка змінена на: {new_dir}", fg='green')
            click.pause()
            continue
        
        if not downloader:
            downloader = YouTubeDownloader()
        
        url = click.prompt("🔗 Введіть посилання на YouTube")
        
        if not url.strip():
            click.secho("❌ Посилання не введено.", fg='red')
            click.pause()
            continue
        
        try:
            if choice == '1':
                downloader.download_video(url, audio_only=False)
            elif choice == '2':
                downloader.download_video(url, audio_only=True)
            elif choice == '3':
                info = downloader.get_video_info(url)
                if info:
                    click.echo()
                    click.secho(f"📹 Назва: {info['title']}", fg='cyan')
                    click.secho(f"⏱️  Тривалість: {info['duration']//60}:{info['duration']%60:02d}", fg='cyan')
                    click.secho(f"👤 Канал: {info['uploader']}", fg='cyan')
                    click.secho(f"📊 Доступних форматів: {info['formats_available']}", fg='cyan')
                else:
                    click.secho("❌ Не вдалося отримати інформацію про відео.", fg='red')
        except KeyboardInterrupt:
            click.secho("\n⏹️  Перервано користувачем.", fg='yellow')
        except Exception as e:
            click.secho(f"❌ Помилка: {str(e)}", fg='red')
        
        click.pause()
if __name__ == "__main__":
    try:
        cli(obj={})
    except KeyboardInterrupt:
        click.echo("\n\n⏹️  Скрипт перервано користувачем.")
        sys.exit(0)
    except Exception as e:
        click.secho(f"❌ Критична помилка: {str(e)}", fg='red')
        sys.exit(1)
