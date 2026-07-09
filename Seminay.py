import os
import sys
import asyncio
import math
import random
import time
import pyaudio
import struct

from google import genai
from google.genai import types

from PyQt6.QtWidgets import (QApplication, QWidget, QSystemTrayIcon, QMenu, 
                             QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QTextEdit, QPushButton, QMessageBox) 
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, pyqtSlot, QSettings
from PyQt6.QtGui import QPainter, QColor, QIcon
from PyQt6.QtCore import QProcess

FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024

MODEL = "models/gemini-2.5-flash-native-audio-latest"

class GeminiWorker(QThread):
    state_changed = pyqtSignal(str)  # SPEAKING, THINKING, IDLE
    connection_dropped = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = True
        self.session = None
        self.audio_in_queue = None
        self.out_queue = None
        self.mic_muted = False
        self.loop = None
        self.current_state = "IDLE"

    def run(self):
        self.pya_in = pyaudio.PyAudio()   
        self.pya_out = pyaudio.PyAudio()  
        
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(self.main_loop())
        except Exception:
            is_restarting = QSettings("SeminayAI", "SeminayAsistan").value("is_restarting", False)
            if self.running and not is_restarting:
                self.connection_dropped.emit()
        finally:
            self.pya_in.terminate()
            self.pya_out.terminate()

    async def main_loop(self):
        settings = QSettings("SeminayAI", "SeminayAsistan")
        api_key = settings.value("api_key", "")
        voice_name = settings.value("voice", "")
        system_instruction = settings.value("system_instruction", "")

        client = genai.Client(api_key=api_key, http_options={"api_version": "v1alpha"})

        voice_config = None
        if voice_name:
            voice_config = types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice_name)
            )

        config = types.LiveConnectConfig(
            system_instruction=system_instruction if system_instruction else None,
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(voice_config=voice_config) if voice_config else None,
            enable_affective_dialog=True,
            media_resolution="MEDIA_RESOLUTION_MEDIUM",
            context_window_compression=types.ContextWindowCompressionConfig(
                trigger_tokens=104857,   
                sliding_window=types.SlidingWindow(target_tokens=52428),
            ),
        )

        async with client.aio.live.connect(model=MODEL, config=config) as session:
            self.session = session
            self.audio_in_queue = asyncio.Queue()
            self.out_queue = asyncio.Queue(maxsize=50)

            async with asyncio.TaskGroup() as tg:
                self.send_task = tg.create_task(self.send_realtime())
                self.mic_task = tg.create_task(self.listen_audio())
                self.receive_task = tg.create_task(self.receive_audio())
                self.play_task = tg.create_task(self.play_audio())

                while self.running:
                    await asyncio.sleep(0.2)

    async def send_realtime(self):
        while self.running:
            msg = await self.out_queue.get()
            if self.session:
                await self.session.send(input=msg)

    async def listen_audio(self):
        def open_mic_stream():
            mic_info = self.pya_in.get_default_input_device_info()
            return self.pya_in.open(
                format=FORMAT, channels=CHANNELS, rate=SEND_SAMPLE_RATE,
                input=True, input_device_index=mic_info["index"], frames_per_buffer=CHUNK_SIZE
            )

        stream = await asyncio.to_thread(open_mic_stream)
        
        try:
            while self.running:
                if self.mic_muted:
                    await asyncio.sleep(0.1)
                    continue
                
                data = await asyncio.to_thread(stream.read, CHUNK_SIZE, exception_on_overflow=False)
                
                if self.current_state == "SPEAKING":
                    continue
                
                if self.current_state != "SPEAKING" and not self.mic_muted:
                    count = len(data) // 2
                    if count > 0:
                        shorts = struct.unpack(f"{count}h", data)
                        max_amplitude = max(abs(s) for s in shorts)
                        
                        if max_amplitude > 800 and self.current_state == "IDLE":
                            self.current_state = "THINKING"
                            self.state_changed.emit("THINKING")

                await self.out_queue.put({"data": data, "mime_type": "audio/pcm"})
        finally:
            stream.stop_stream()
            stream.close()

    async def receive_audio(self):
        while self.running:
            if self.session:
                async for response in self.session.receive():
                    if response.server_content and response.server_content.model_turn:
                        for part in response.server_content.model_turn.parts:
                            if part.inline_data and self.running:
                                self.audio_in_queue.put_nowait(part.inline_data.data)
                    
                    if response.server_content and response.server_content.turn_complete:
                        if self.audio_in_queue.empty() and self.current_state == "THINKING":
                            self.current_state = "IDLE"
                            self.state_changed.emit("IDLE")

    async def play_audio(self):
        stream = await asyncio.to_thread(
            self.pya_out.open, format=FORMAT, channels=CHANNELS, rate=RECEIVE_SAMPLE_RATE, output=True
        )
        try:
            while self.running:
                bytestream = await self.audio_in_queue.get()
                
                self.current_state = "SPEAKING"
                self.state_changed.emit("SPEAKING") 
                
                await asyncio.to_thread(stream.write, bytestream)
                
                if self.audio_in_queue.empty():
                    self.current_state = "IDLE"
                    self.state_changed.emit("IDLE")
        finally:
            stream.stop_stream()
            stream.close()

    def send_text_input(self, text):
        if self.loop and self.session:
            self.current_state = "THINKING"
            asyncio.run_coroutine_threadsafe(
                self.session.send(input=text, end_of_turn=True), self.loop
            )

    def toggle_mic(self):
        self.mic_muted = not self.mic_muted
        if self.mic_muted:
            self.current_state = "IDLE"
        return self.mic_muted

    def stop(self):
        self.running = False
        if hasattr(self, 'send_task'): self.send_task.cancel()
        if hasattr(self, 'mic_task'): self.mic_task.cancel()
        if hasattr(self, 'receive_task'): self.receive_task.cancel()
        if hasattr(self, 'play_task'): self.play_task.cancel()
        if self.loop:
            self.loop.stop()


class EqualizerBar(QWidget):
    def __init__(self, color="#ffffff", parent=None):
        super().__init__(parent)
        self.bar_color = QColor(color)
        self.setFixedSize(60, 22)
        self.values = [10, 10, 10]
        self.state = "IDLE"
        self.wave_counter = 0

    def set_state(self, state):
        self.state = state
        self.update()

    def update_animation(self):
        if self.state == "THINKING":
            self.values = [10, 10, 10]
            self.values[self.wave_counter % 3] = 18
            self.wave_counter += 1
        elif self.state == "SPEAKING":
            self.values = [random.randint(6, 22) for _ in range(3)]
        elif self.state == "IDLE":
            t = time.time() * 4 
            self.values = [13 + (3 * math.sin(t + (i * 0.4))) for i in range(3)]
        else:
            self.values = [10, 10, 10]
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(self.bar_color)
        p.setPen(Qt.PenStyle.NoPen)
        
        if self.state == "LISTENING":
            for i in range(5): 
                p.drawEllipse(i * 12, 12, 8, 8)
        elif self.state == "THINKING":
            for i, v in enumerate(self.values): 
                p.drawEllipse((i+1)*12, 22-int(v), 8, 8)
        else:
            for i, v in enumerate(self.values): 
                v_int = int(v)
                p.drawRoundedRect((i+1)*12, 22-v_int, 8, v_int, 4, 4)

        is_muted = self.window().worker.mic_muted if hasattr(self.window(), 'worker') else False
        base_color = QColor("#ff0000") if is_muted else QColor("#00ff00")
        
        p.setPen(Qt.PenStyle.NoPen)
        
        p.setBrush(QColor(0, 0, 0, 150))
        p.drawEllipse(54, 0, 7, 7) 
        
        p.setBrush(QColor(base_color.red(), base_color.green(), base_color.blue(), 240))
        p.drawEllipse(55, 1, 5, 5) 
        
        p.setBrush(base_color)
        p.drawEllipse(56, 2, 3, 3)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            if 50 <= pos.x() <= 64 and 0 <= pos.y() <= 12:
                self.window().toggle_mic()
                self.update()
                event.accept() 
                return

        event.ignore()

class SettingsWindow(QWidget):
    def __init__(self, full_mode=False):
        super().__init__()
        self.full_mode = full_mode
        self.settings = QSettings("SeminayAI", "SeminayAsistan")
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setStyleSheet("""
            QWidget { color: white; font-family: Arial; }
            QLineEdit, QComboBox, QTextEdit {
                background-color: #1e1e1e; color: white; 
                border: 1px solid #3a3a3a; border-radius: 8px; padding: 6px;
            }
            QComboBox QAbstractItemView, QMenu {
                background-color: #1e1e1e; color: white; border: 1px solid #3a3a3a;
            }
            QMenu::item:selected { background-color: #3a3a3a; }
            QPushButton { border-radius: 8px; padding: 8px; }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.current_lang = self.settings.value("language", "TR")

        texts = {
            "TR": {
                "title_setup": "Seminay Kurulum", "title_settings": "Seminay Ayarlar",
                "api_lbl": "Gemini API Key:", "lang_lbl": "Uygulama Dili / Language:",
                "voice_lbl": "Ses Tonu Seçimi:", "prompt_lbl": "Kişilik Talimatı (Prompt):", 
                "default_voice": "Varsayılan (Gemini Standart)",
                "save_start": "Kaydet ve Başlat", "save_restart": "Kaydet ve Yeniden Başlat", "cancel": "İptal",
                "exit": "Çıkış"
            },
            "EN": {
                "title_setup": "Seminay Setup", "title_settings": "Seminay Settings",
                "api_lbl": "Gemini API Key:", "lang_lbl": "Language / Uygulama Dili:",
                "voice_lbl": "Voice Selection:", "prompt_lbl": "System Instructions (Prompt):", 
                "default_voice": "Default (Gemini Standard)",
                "save_start": "Save and Start", "save_restart": "Save and Restart", "cancel": "Cancel",
                "exit": "Exit"
            }
        }
        t = texts.get(self.current_lang, texts["TR"])

        title_text = t["title_settings"] if self.full_mode else t["title_setup"]
        title = QLabel(title_text)
        title.setStyleSheet("font-size: 14px; font-weight: bold; border: none; background: transparent;")
        layout.addWidget(title)

        layout.addWidget(QLabel(t["lang_lbl"], styleSheet="color: #aaaaaa; font-size: 11px; border: none; background: transparent;"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("Türkçe 🇹🇷", "TR")
        self.lang_combo.addItem("English 🇺🇸", "EN")
        self.lang_combo.setCurrentIndex(0 if self.current_lang == "TR" else 1)
        layout.addWidget(self.lang_combo)

        layout.addWidget(QLabel(t["api_lbl"], styleSheet="color: #aaaaaa; font-size: 11px; border: none; background: transparent;"))
        self.api_input = QLineEdit()
        self.api_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_input.setText(self.settings.value("api_key", ""))
        layout.addWidget(self.api_input)

        if self.full_mode:
            self.setFixedSize(290, 420) 
            
            layout.addWidget(QLabel(t["voice_lbl"], styleSheet="color: #aaaaaa; font-size: 11px; border: none; background: transparent;"))
            self.voice_combo = QComboBox()
            self.voice_combo.addItem(t["default_voice"], "")
            
            is_tr = (self.current_lang == "TR")

            self.voice_combo.addItem("--- Kadın Sesleri ---" if is_tr else "--- Female Voices ---", None)
            female_voices = [
                ("Achernar", "Soft, Higher pitch", "Yumuşak, Yüksek perde"),
                ("Aoede", "Breezy, Middle pitch", "Ferah, Orta perde"),
                ("Autone", "Bright, Middle pitch", "Parlak, Orta perde"),
                ("Callirrhoe", "Easy-going, Middle pitch", "Rahat, Orta perde"),
                ("Despina", "Smooth, Middle pitch", "Pürüzsüz, Orta perde"),
                ("Erinome", "Clear, Middle pitch", "Berrak, Orta perde"),
                ("Gacrux", "Mature, Middle pitch", "Olgun, Orta perde"),
                ("Kore", "Firm, Middle pitch", "Yumuşak, Orta perde"),
                ("Laomedeia", "Upbeat, Higher pitch", "Neşeli, Yüksek perde"),
                ("Leda", "Youthful, Higher pitch", "Genç, Yüksek perde"),
                ("Sulafat", "Warm, Middle pitch", "Sıcak, Orta perde"),
                ("Vindemiatrix", "Middle pitch", "Orta perde"),
                ("Zephyr", "Bright, Higher pitch", "Parlak, Yüksek perde")
            ]
            for name, eng, tr in female_voices:
                self.voice_combo.addItem(f"{name} ({tr if is_tr else eng})", name)

            self.voice_combo.addItem("--- Erkek Sesleri ---" if is_tr else "--- Male Voices ---", None)
            male_voices = [
                ("Achird", "Friendly, Lower middle pitch", "Dost canlısı, Alt orta perde"),
                ("Algieba", "Smooth, Lower pitch", "Pürüzsüz, Düşük perde"),
                ("Algenib", "Gravelly, Lower pitch", "Çakıllı, Düşük perde"),
                ("Alnilam", "Firm, Lower middle pitch", "Sağlam, Alt orta perde"),
                ("Charon", "Informative, Lower pitch", "Bilgilendirici, Düşük perde"),
                ("Enceladus", "Breathy, Lower pitch", "Nefesli, Düşük perde"),
                ("Fenrir", "Excitable, Lower middle pitch", "Heyecanlı, Alt orta perde"),
                ("Iapetus", "Clear, Lower middle pitch", "Berrak, Alt orta perde"),
                ("Orus", "Firm, Lower middle pitch", "Sağlam, Alt orta perde"),
                ("Puck", "Upbeat, Middle pitch", "Neşeli, Orta perde"),
                ("Pulcherrima", "Forward, Middle pitch", "İlerici, Orta perde"),
                ("Rasalgethi", "Informative, Middle pitch", "Bilgilendirici, Orta perde"),
                ("Sadachbia", "Lively, Lower pitch", "Canlı, Düşük perde"),
                ("Sadaltager", "Knowledge, Middle pitch", "Bilgili, Orta perde"),
                ("Schedar", "Even, Lower middle pitch", "Dengeli, Alt orta perde"),
                ("Umbriel", "Easy-going, Lower middle pitch", "Rahat, Alt orta perde"),
                ("Zubenelgenubi", "Casual, Lower middle pitch", "Rahat, Alt orta perde")
            ]
            for name, eng, tr in male_voices:
                self.voice_combo.addItem(f"{name} ({tr if is_tr else eng})", name)

            saved_voice = self.settings.value("voice", "")
            index = self.voice_combo.findData(saved_voice)
            if index != -1:
                self.voice_combo.setCurrentIndex(index)
            layout.addWidget(self.voice_combo)

            layout.addWidget(QLabel(t["prompt_lbl"], styleSheet="color: #aaaaaa; font-size: 11px; border: none; background: transparent;"))
            self.instruction_input = QTextEdit()
            self.instruction_input.setText(self.settings.value("system_instruction", ""))
            layout.addWidget(self.instruction_input)
        else:
            self.setFixedSize(290, 220) 

        btn_layout = QHBoxLayout()
        btn_text = t["save_restart"] if self.full_mode else t["save_start"]
        self.save_btn = QPushButton(btn_text)
        self.save_btn.setStyleSheet("background-color: #ffffff; color: black; font-weight: bold;")
        self.save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(self.save_btn)

        if self.full_mode:
            self.cancel_btn = QPushButton(t["cancel"])
            self.cancel_btn.setStyleSheet("background-color: #2c2c2c; color: white; border: 1px solid #3a3a3a;")
            self.cancel_btn.clicked.connect(self.close_settings)
            btn_layout.addWidget(self.cancel_btn)
        else:
            self.exit_btn = QPushButton(t["exit"])
            self.exit_btn.setStyleSheet("background-color: #2c2c2c; color: white; border: 1px solid #3a3a3a;")
            self.exit_btn.clicked.connect(QApplication.instance().quit)
            btn_layout.addWidget(self.exit_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.reposition_to_corner()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(QColor("#121212"))
        p.setPen(QColor("#2c2c2c"))
        p.drawRoundedRect(0, 0, self.width() - 1, self.height() - 1, 18, 18)

    def reposition_to_corner(self):
        s = QApplication.primaryScreen().availableGeometry()
        self.move(s.width() - self.width() - 15, s.height() - self.height() - 45)

    def save_settings(self):
        self.settings.setValue("language", self.lang_combo.currentData())
        self.settings.setValue("api_key", self.api_input.text().strip())
        self.settings.setValue("is_restarting", True)
        
        if self.full_mode:
            self.settings.setValue("voice", self.voice_combo.currentData())
            self.settings.setValue("system_instruction", self.instruction_input.toPlainText().strip())
        else:
            self.settings.setValue("voice", "")
            self.settings.setValue("system_instruction", "")
            
        self.settings.sync()
        
        lang = self.lang_combo.currentData()
        
        if lang == "EN":
            title = "Seminay - Restarting"
            text = "Settings saved."
            info = "The application is restarting to apply changes."
        else:
            title = "Seminay - Yeniden Başlatılıyor"
            text = "Ayarlar kaydedildi."
            info = "Değişikliklerin uygulanması için program yeniden başlatılıyor."
        
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setInformativeText(info)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        msg.setStyleSheet("""
            QMessageBox { background-color: #121212; }
            QLabel { color: white; }
            QPushButton { 
                background-color: #ffffff; color: black; 
                border-radius: 5px; padding: 5px 15px; font-weight: bold;
            }
        """)
        
        msg.exec()
        
        QProcess.startDetached(sys.executable, sys.argv)
        QApplication.quit()

    def close_settings(self):
        self.close()
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, SeminayKapsul):
                widget.show()


class SeminayKapsul(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("SeminayAI", "SeminayAsistan")
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(120, 120)

        self.worker = GeminiWorker()
        self.worker.state_changed.connect(self.on_state_changed)
        self.worker.connection_dropped.connect(self.show_disconnect_warning)
        self.worker.start()

        self.chat_input = QLineEdit(self)
        self.chat_input.setGeometry(10, 5, 100, 32)
        self.chat_input.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1a1a1a, stop:1 #000000); "
            "border: 1px solid #333333; border-radius: 10px; color: white; padding-left: 5px; font-family: Arial; font-size: 11px;"
        )
        self.chat_input.returnPressed.connect(self.send_chat)
        self.chat_input.hide()

        self.capsule_body = QWidget(self)
        self.capsule_body.setFixedSize(100, 36)
        self.capsule_body.move(10, 45)
        self.capsule_body.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1a1a1a, stop:1 #000000); "
            "border-radius: 18px;"
        )

        self.equalizer = EqualizerBar(color="#ffffff", parent=self.capsule_body)
        self.equalizer.move(20, 7)

        self.setup_tray()

        self.ani_timer = QTimer()
        self.ani_timer.timeout.connect(self.equalizer.update_animation)
        self.ani_timer.start(120)

        self.reposition_to_corner()
        self.show()

    def setup_tray(self):
        lang = self.settings.value("language", "TR")
        
        menu_texts = {
            "TR": {"show": "Göster", "settings": "Ayarlar", "exit": "Çıkış"},
            "EN": {"show": "Show", "settings": "Settings", "exit": "Exit"}
        }
        m = menu_texts.get(lang, menu_texts["TR"])

        self.tray_icon = QSystemTrayIcon(self)
        
        icon_path = os.path.join(os.getcwd(), "icon.ico")
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            self.tray_icon.setIcon(QApplication.style().standardIcon(QApplication.style().StandardPixmap.SP_ComputerIcon))
        
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #3a3a3a;
            }
            QMenu::item:selected {
                background-color: #3a3a3a;
            }
        """)
        
        menu.addAction(m["show"], self.show_kapsul)
        menu.addAction(m["settings"], self.open_settings)  
        menu.addAction(m["exit"], self.safe_exit)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda pos: menu.exec(self.mapToGlobal(pos)))

    def open_settings(self):
        self.hide() 
        self.settings_win = SettingsWindow(full_mode=True)
        self.settings_win.show()

    def safe_exit(self):
        self.hide()
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
        
        self.worker.running = False
        QTimer.singleShot(500, self._final_terminate)

    def _final_terminate(self):
        QApplication.instance().quit()
        os._exit(0)

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_kapsul()

    def show_kapsul(self):
        self.show()
        self.raise_()

    @pyqtSlot()
    def show_disconnect_warning(self):
        self.on_state_changed("IDLE") 
        
        lang = self.settings.value("language", "TR")
        
        if lang == "EN":
            title = "Seminay - Connection Lost"
            text = "Connection to Google servers lost."
            info = "Please restart the application to continue."
        else:
            title = "Seminay - Bağlantı Koptu"
            text = "Google sunucularıyla iletişim kesildi."
            info = "Sohbete devam edebilmek için lütfen uygulamayı yeniden başlatın."

        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setInformativeText(info)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        msg.setStyleSheet("""
            QMessageBox { background-color: #121212; }
            QLabel { color: white; }
            QPushButton { 
                background-color: #ffffff; color: black; 
                border-radius: 5px; padding: 5px 15px; font-weight: bold;
            }
        """)
        msg.exec()

    def reposition_to_corner(self):
        s = QApplication.primaryScreen().availableGeometry()
        self.move(s.width() - 115, s.height() - 85)

    @pyqtSlot(str)
    def on_state_changed(self, state):
        self.equalizer.set_state(state)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            diff = event.globalPosition().toPoint() - self._drag_pos
            self.move(self.pos() + diff)
            self._drag_pos = event.globalPosition().toPoint()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.chat_input.isVisible():
                self.chat_input.hide()
            else:
                self.chat_input.show()
                self.chat_input.setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
        super().keyPressEvent(event)

    def send_chat(self):
        text = self.chat_input.text().strip()
        if text:
            self.on_state_changed("THINKING")
            self.worker.current_state = "THINKING"
            self.worker.send_text_input(text)
            self.chat_input.clear()

    def toggle_mic(self):
        muted = self.worker.toggle_mic()
        if muted:
            self.on_state_changed("IDLE")
        self.equalizer.update()

    def closeEvent(self, event):
        self.safe_exit()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    settings = QSettings("SeminayAI", "SeminayAsistan")

    if not settings.value("api_key"):
        initial_setup = SettingsWindow(full_mode=False)
        initial_setup.show()
    else:
        kapsul = SeminayKapsul()
        
    sys.exit(app.exec())