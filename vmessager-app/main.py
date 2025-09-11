import sys
import hashlib
import asyncio
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton,
    QLabel, QScrollArea, QFrame, QSizePolicy, QHBoxLayout
)
from PyQt5.QtMultimedia import QSound
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5 import QtCore
# pip install qasync
import qasync

class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Async Chat Template")
        self.setStyleSheet("background-color: black; color: white;")
        self.resize(600, 500)

        # Font
        font_id = QFontDatabase.addApplicationFont("joystix.otf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.custom_font = QFont(font_family, 10)
        else:
            self.custom_font = QFont("Arial", 10)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Chat area
        self.chat_area_layout = QVBoxLayout()
        self.chat_area_layout.setSpacing(5)
        self.chat_area_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        scroll_widget = QWidget()
        scroll_widget.setLayout(self.chat_area_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(scroll_widget)
        self.scroll_area.setStyleSheet("background-color: black;")
        layout.addWidget(self.scroll_area)

        # Input fields
        self.sender_label = QLabel("Ty jako odbiorca: Anonim")
        self.sender_label.setFont(self.custom_font)
        layout.addWidget(self.sender_label)

        self.external_sender_input = QLineEdit()
        self.external_sender_input.setPlaceholderText("Odbiorca")
        self.external_sender_input.setStyleSheet("background-color: black; color: white; border: 1px solid white;")
        self.external_sender_input.setFont(self.custom_font)
        layout.addWidget(self.external_sender_input)

        self.message_input = QTextEdit()
        self.message_input.setFixedHeight(60)
        self.message_input.setStyleSheet("background-color: black; color: white; border: 1px solid white;")
        self.message_input.setFont(self.custom_font)
        layout.addWidget(self.message_input)

        self.send_button = QPushButton("Wyślij")
        self.send_button.setStyleSheet("background-color: black; color: white; border: 1px solid white;")
        self.send_button.setFont(self.custom_font)
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)

        # Pierwsza wiadomość systemowa
        self.send_message(sender_override="System", message_override="Async chat started!", direction="incoming")

    def get_color_from_text(self, text):
        hash_int = int(hashlib.md5(text.encode()).hexdigest()[:6], 16)
        r = (hash_int >> 16) & 0xFF
        g = (hash_int >> 8) & 0xFF
        b = hash_int & 0xFF
        return f'rgb({r},{g},{b})'

    def send_message(self, sender_override=None, message_override=None, direction="outgoing"):
        sender_input = sender_override if sender_override else self.external_sender_input.text().strip()
        message = message_override if message_override else self.message_input.toPlainText().strip()
        if not message:
            return

        color = self.get_color_from_text(sender_input)

        frame = QFrame()
        h_layout = QHBoxLayout()
        frame.setLayout(h_layout)

        bubble = QFrame()
        v_layout = QVBoxLayout()
        v_layout.setSpacing(2)
        bubble.setLayout(v_layout)
        bubble.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        if direction == "outgoing":
            bubble.setStyleSheet("background-color: #222; border-radius: 5px; padding: 5px;")
            h_layout.addStretch()
            h_layout.addWidget(bubble)
        else:
            bubble.setStyleSheet("background-color: #444; border-radius: 5px; padding: 5px;")
            h_layout.addWidget(bubble)
            h_layout.addStretch()

        sender_label = QLabel(sender_input)
        sender_label.setFont(self.custom_font)
        sender_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        v_layout.addWidget(sender_label)

        message_label = QLabel(message)
        message_label.setFont(self.custom_font)
        message_label.setStyleSheet("color: white;" if direction == "outgoing" else "color: #FFFF88;")
        message_label.setWordWrap(True)
        v_layout.addWidget(message_label)

        self.chat_area_layout.addWidget(frame)
        v_scroll_bar = self.scroll_area.verticalScrollBar()
        if v_scroll_bar:
            v_scroll_bar.setValue(v_scroll_bar.maximum())

        if direction == "outgoing":
            self.message_input.clear()
            self.external_sender_input.clear()
        else:
            QSound.play("sound.wav")


# ----------------- ASYNC BOT -----------------
async def bot_loop(window: ChatApp):
    """Przykładowy bot async – możesz tu podpiąć sieć albo ICP"""
    while True:
        await asyncio.sleep(5)  # co 5 sekund sprawdza coś
        # jeśli nie ma nowych wiadomości → nie rób nic
        # tu dla testu zawsze wysyła przykładową wiadomość
        window.send_message(sender_override="Bot", message_override="Async test message", direction="incoming")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ChatApp()
    window.show()

    loop = qasync.QEventLoop(app)  # integracja asyncio + PyQt
    asyncio.set_event_loop(loop)

    with loop:
        asyncio.ensure_future(bot_loop(window))
        loop.run_forever()
