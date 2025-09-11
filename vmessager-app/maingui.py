
import sys
import asyncio
from pathlib import Path
import hashlib
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton,
    QLabel, QScrollArea, QFrame, QSizePolicy, QHBoxLayout, QStatusBar
)
from PyQt5.QtMultimedia import QSound
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5 import QtCore
import qasync

from ic_connector import VMessageConnector

# Ścieżka do pliku tożsamości
IDENTITY_PEM_PATH = Path(__file__).parent / "identity.pem"

class ChatApp(QWidget):
    # Sygnał do dodawania wiadomości z innych wątków/zadań async
    message_received_signal = QtCore.pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()
        self.connector = VMessageConnector(IDENTITY_PEM_PATH)
        self.init_ui()
        self.message_received_signal.connect(self.add_message_bubble)

    def init_ui(self):
        self.setWindowTitle("V-Messenger GUI")
        self.setStyleSheet("background-color: #1a1a1a; color: white;")
        self.resize(700, 600)

        # Font
        font_id = QFontDatabase.addApplicationFont("joystix.otf")
        font_family = "Arial"
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.custom_font = QFont(font_family, 10)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Chat area
        self.chat_area_layout = QVBoxLayout()
        self.chat_area_layout.setSpacing(10)
        self.chat_area_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.chat_area_layout)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(scroll_widget)
        self.scroll_area.setStyleSheet("background-color: #111; border: none;")
        layout.addWidget(self.scroll_area)

        # Input fields
        self.recipient_input = QLineEdit()
        self.recipient_input.setPlaceholderText("Wpisz Principal ID odbiorcy...")
        self.recipient_input.setStyleSheet("background-color: #333; color: white; border: 1px solid #555; padding: 5px;")
        self.recipient_input.setFont(self.custom_font)
        layout.addWidget(self.recipient_input)

        self.message_input = QTextEdit()
        self.message_input.setFixedHeight(60)
        self.message_input.setPlaceholderText("Wpisz swoją wiadomość...")
        self.message_input.setStyleSheet("background-color: #333; color: white; border: 1px solid #555; padding: 5px;")
        self.message_input.setFont(self.custom_font)
        layout.addWidget(self.message_input)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.send_button = QPushButton("Wyślij")
        self.send_button.setStyleSheet("background-color: #007acc; color: white; border: none; padding: 8px;")
        self.send_button.setFont(self.custom_font)
        self.send_button.clicked.connect(self.on_send_clicked)
        buttons_layout.addWidget(self.send_button)

        self.check_button = QPushButton("Sprawdź wiadomości")
        self.check_button.setStyleSheet("background-color: #555; color: white; border: none; padding: 8px;")
        self.check_button.setFont(self.custom_font)
        self.check_button.clicked.connect(self.on_check_clicked)
        buttons_layout.addWidget(self.check_button)
        layout.addLayout(buttons_layout)

        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("color: #aaa;")
        my_principal = self.connector.get_my_principal()
        self.status_bar.showMessage(f"Twój Principal: {my_principal[:15]}...")
        layout.addWidget(self.status_bar)

        # Pierwsza wiadomość systemowa
        self.add_message_bubble("System", "Witaj w V-Messenger. Automatyczne sprawdzanie wiadomości aktywne.", "system")

    def get_color_from_text(self, text):
        hash_int = int(hashlib.md5(text.encode()).hexdigest()[:6], 16)
        r = (hash_int & 0xFF0000) >> 16
        g = (hash_int & 0x00FF00) >> 8
        b = hash_int & 0x0000FF
        return f'rgb({(r % 155) + 100},{(g % 155) + 100},{(b % 155) + 100})'

    @QtCore.pyqtSlot(str, str, str)
    def add_message_bubble(self, sender, message, direction):
        frame = QFrame()
        h_layout = QHBoxLayout()
        frame.setLayout(h_layout)

        bubble = QFrame()
        v_layout = QVBoxLayout()
        bubble.setLayout(v_layout)
        
        sender_label = QLabel(sender)
        sender_label.setFont(self.custom_font)
        sender_label.setWordWrap(True)

        message_label = QLabel(message)
        message_label.setFont(self.custom_font)
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        if direction == "outgoing":
            bubble.setStyleSheet("background-color: #007acc; border-radius: 10px; padding: 8px;")
            sender_label.setStyleSheet("color: white; font-weight: bold;")
            message_label.setStyleSheet("color: white;")
            h_layout.addStretch()
            h_layout.addWidget(bubble)
        elif direction == "incoming":
            color = self.get_color_from_text(sender)
            bubble.setStyleSheet(f"background-color: #333; border-radius: 10px; padding: 8px;")
            sender_label.setStyleSheet(f"color: {color}; font-weight: bold;")
            message_label.setStyleSheet("color: white;")
            h_layout.addWidget(bubble)
            h_layout.addStretch()
            QSound.play("sound.wav")
        else: # System message
            bubble.setStyleSheet("background-color: transparent; border: 1px solid #555; border-radius: 5px; padding: 5px;")
            sender_label.setStyleSheet("color: #aaa; font-weight: bold;")
            message_label.setStyleSheet("color: #aaa; font-style: italic;")
            h_layout.addWidget(bubble)

        v_layout.addWidget(sender_label)
        v_layout.addWidget(message_label)
        self.chat_area_layout.addWidget(frame)
        
        # Auto-scroll
        def scroll_to_bottom():
            scrollbar = self.scroll_area.verticalScrollBar()
            if scrollbar is not None:
                scrollbar.setValue(scrollbar.maximum())
        QtCore.QTimer.singleShot(100, scroll_to_bottom)

    def on_send_clicked(self):
        recipient = self.recipient_input.text().strip()
        message = self.message_input.toPlainText().strip()
        if not recipient or not message:
            self.status_bar.showMessage("Błąd: Odbiorca i wiadomość nie mogą być puste.", 3000)
            return
        
        self.add_message_bubble("Ja", message, "outgoing")
        self.message_input.clear()
        
        async def send_task():
            self.status_bar.showMessage("Wysyłanie...")
            result = await self.connector.send_message(recipient, message)
            if isinstance(result, dict) and 'err' in result:
                self.status_bar.showMessage(f"Błąd wysyłania: {result['err']}", 5000)
            else:
                self.status_bar.showMessage(f"Wiadomość wysłana! ({result})", 3000)
        
        asyncio.create_task(send_task())

    def on_check_clicked(self):
        async def check_task():
            self.status_bar.showMessage("Sprawdzanie wiadomości...")
            result = await self.connector.check_messages()
            
            if isinstance(result, dict) and 'err' in result:
                self.status_bar.showMessage(f"Błąd: {result['err']}", 5000)
            elif "Twoja skrzynka jest pusta" in str(result):
                self.status_bar.showMessage(str(result), 3000)
            else:
                self.status_bar.showMessage("Odebrano nową wiadomość!", 3000)
                # Wiadomość ma format "from:PRINCIPAL:message:TRESC"
                try:
                    if isinstance(result, str) and result:
                        parts = result.split(':')
                        sender = parts[1]
                        msg_content = ':'.join(parts[3:])
                        self.message_received_signal.emit(sender, msg_content, "incoming")
                    else:
                        self.message_received_signal.emit("Nieznany nadawca", str(result), "incoming")
                except IndexError:
                    self.message_received_signal.emit("Nieznany nadawca", str(result), "incoming")

        asyncio.create_task(check_task())

async def periodic_message_check(app_window: ChatApp):
    """Pętla w tle do automatycznego sprawdzania wiadomości."""
    while True:
        await asyncio.sleep(15) # Sprawdzaj co 15 sekund
        
        result = await app_window.connector.check_messages()
        if isinstance(result, dict) or (isinstance(result, str) and "Twoja skrzynka jest pusta" in result):
            continue
        else:
            try:
                if result is not None:
                    parts = result.split(':')
                    sender = parts[1]
                    msg_content = ':'.join(parts[3:])
                    app_window.message_received_signal.emit(sender, msg_content, "incoming")
                else:
                    app_window.message_received_signal.emit("Nieznany nadawca", str(result), "incoming")
            except IndexError:
                app_window.message_received_signal.emit("Nieznany nadawca", str(result), "incoming")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = ChatApp()
    window.show()

    # Ustawienie pętli zdarzeń qasync
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    with loop:
        # Uruchomienie pętli w tle
        asyncio.ensure_future(periodic_message_check(window))
        # Uruchomienie głównej pętli aplikacji
        sys.exit(loop.run_forever())
