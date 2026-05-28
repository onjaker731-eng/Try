"""
YouTube Video Downloader - Kivy Version
Мобільний інтерфейс для Android
"""

import os
from datetime import datetime
from pathlib import Path
from threading import Thread

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.togglebutton import ToggleButton

try:
    import yt_dlp
except ImportError:
    pass

# Налаштування вікна
Window.size = (360, 640)

DEFAULT_DOWNLOAD_DIR = "downloads"


class YouTubeDownloaderApp(App):
    """Основний клас для Kivy додатку"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "YouTube Downloader"
        self.downloader = None
        self.is_downloading = False
        
    def build(self):
        """Побудова UI"""
        # Головна розкладка
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Заголовок
        title_label = Label(
            text='🎬 YouTube Downloader',
            size_hint_y=0.1,
            font_size='24sp',
            bold=True
        )
        main_layout.add_widget(title_label)
        
        # Полотно для введення URL
        url_layout = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=5)
        url_layout.add_widget(Label(text='YouTube URL:', size_hint_y=0.3))
        self.url_input = TextInput(
            multiline=False,
            hint_text='https://www.youtube.com/watch?v=...',
            size_hint_y=0.7
        )
        url_layout.add_widget(self.url_input)
        main_layout.add_widget(url_layout)
        
        # Опції завантаження
        options_layout = BoxLayout(size_hint_y=0.12, spacing=5)
        self.audio_only_btn = ToggleButton(text='Audio Only\n(MP3)', size_hint_x=0.5)
        self.video_btn = ToggleButton(text='Video + Audio\n(MP4)', state='down', size_hint_x=0.5)
        
        # Пов'язуємо кнопки
        self.audio_only_btn.bind(state=self.on_audio_toggle)
        self.video_btn.bind(state=self.on_video_toggle)
        
        options_layout.add_widget(self.audio_only_btn)
        options_layout.add_widget(self.video_btn)
        main_layout.add_widget(options_layout)
        
        # Кнопки дій
        buttons_layout = BoxLayout(size_hint_y=0.12, spacing=5)
        
        info_btn = Button(text='ℹ️ Info', size_hint_x=0.33)
        info_btn.bind(on_press=self.show_info)
        
        download_btn = Button(text='📥 Download', size_hint_x=0.33)
        download_btn.bind(on_press=self.download_video)
        
        clear_btn = Button(text='🗑️ Clear', size_hint_x=0.34)
        clear_btn.bind(on_press=self.clear_url)
        
        buttons_layout.add_widget(info_btn)
        buttons_layout.add_widget(download_btn)
        buttons_layout.add_widget(clear_btn)
        main_layout.add_widget(buttons_layout)
        
        # Прогрес бар
        self.progress = ProgressBar(value=0, size_hint_y=0.08)
        main_layout.add_widget(self.progress)
        
        # Лог вывод
        log_layout = BoxLayout(orientation='vertical', size_hint_y=0.48)
        scroll = ScrollView()
        self.log_label = Label(
            text='ログ будет здесь...',
            size_hint_y=None,
            markup=True
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        scroll.add_widget(self.log_label)
        log_layout.add_widget(scroll)
        main_layout.add_widget(log_layout)
        
        return main_layout
    
    def on_audio_toggle(self, instance, value):
        """Обробляє вибір аудіо"""
        if value == 'down':
            self.video_btn.state = 'normal'
    
    def on_video_toggle(self, instance, value):
        """Обробляє вибір відео"""
        if value == 'down':
            self.audio_only_btn.state = 'normal'
    
    def log(self, message):
        """Додає повідомлення в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_label.text += f"\n[{timestamp}] {message}"
        # Скролимо вниз
        self.log_label.parent.scroll_y = 0
    
    def clear_url(self, instance):
        """Очищає поле введення"""
        self.url_input.text = ''
        self.log_label.text = 'URL очищено.'
    
    def show_info(self, instance):
        """Показує інформацію про відео"""
        url = self.url_input.text.strip()
        if not url:
            self.log("❌ Введіть URL!")
            return
        
        Thread(target=self._get_info_thread, args=(url,), daemon=True).start()
    
    def _get_info_thread(self, url):
        """Потік для отримання інформації"""
        try:
            self.log("🔍 Отримую інформацію...")
            ydl_opts = {"quiet": True, "no_warnings": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                uploader = info.get('uploader', 'Unknown')
                formats_count = len(info.get('formats', []))
                
                minutes, seconds = divmod(duration, 60)
                
                self.log(f"✅ Название: {title}")
                self.log(f"⏱️ Тривалость: {minutes}:{seconds:02d}")
                self.log(f"👤 Канал: {uploader}")
                self.log(f"📊 Форматів: {formats_count}")
        except Exception as e:
            self.log(f"❌ Ошибка: {str(e)}")
    
    def download_video(self, instance):
        """Запускає завантаження"""
        url = self.url_input.text.strip()
        if not url:
            self.log("❌ Введіть URL!")
            return
        
        if self.is_downloading:
            self.log("⏳ Завантаження вже в процесі...")
            return
        
        audio_only = self.audio_only_btn.state == 'down'
        Thread(
            target=self._download_thread,
            args=(url, audio_only),
            daemon=True
        ).start()
    
    def _download_thread(self, url, audio_only):
        """Потік для завантаження"""
        self.is_downloading = True
        try:
            self.log("🎬 Початок завантаження...")
            self.progress.value = 0
            
            output_dir = Path(DEFAULT_DOWNLOAD_DIR)
            output_dir.mkdir(exist_ok=True)
            
            ydl_opts = {
                'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
            }
            
            if audio_only:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
                self.log("🔊 Режим: Тільки аудіо (MP3)")
            else:
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
                ydl_opts['merge_output_format'] = 'mp4'
                self.log("🎥 Режим: Відео + Аудіо (MP4)")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                self.log(f"✅ Завершено!")
                self.log(f"💾 Файл: {filename}")
                self.progress.value = 100
        except Exception as e:
            self.log(f"❌ Помилка: {str(e)}")
            self.progress.value = 0
        finally:
            self.is_downloading = False


if __name__ == '__main__':
    YouTubeDownloaderApp().run()
