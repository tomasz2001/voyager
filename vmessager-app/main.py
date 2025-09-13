import sys
import hashlib
import asyncio
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton,
    QLabel, QScrollArea, QFrame, QSizePolicy, QHBoxLayout
)
from PyQt5.QtMultimedia import QSound
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt
import qasync  

from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import encode, Types
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
import os

canisterId = "bkxiq-haaaa-aaaad-abo5q-cai"
identity_file = "identity.pem"
vms_repete = "welcome to vmessager please say to me to be more help"
me = ""
if os.path.exists(identity_file):
    with open(identity_file, "r") as f:
        private_key_pem = f.read().strip()
else:
    private_key_pem = ""


def generate_new_identity():
    private_key = ed25519.Ed25519PrivateKey.generate()
    pem_pkcs8 = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
    with open(identity_file, "w") as f:
        f.write(pem_pkcs8)
    return pem_pkcs8


def load_identity_from_pem(pem_data):
    global private_key_pem
    if not pem_data or not pem_data.startswith("-----BEGIN PRIVATE KEY-----"):
        pem_data = generate_new_identity()
        private_key_pem = pem_data.strip()
    return Identity.from_pem(pem_data)


async def icpcon(metode, items=None):
    client = Client(url='https://ic0.app')
    identity = load_identity_from_pem(private_key_pem)
    agent = Agent(identity, client)
    try:
        if metode == 'glue':
            param_glue = [{'type': Types.Vec(Types.Text), 'value': items}]
            result = await agent.query_raw_async(canisterId, "glue_get", encode(param_glue))
            if isinstance(result, list) and len(result) > 0 and 'value' in result[0]:
                return result[0]['value']
        if metode == 'gluePUSH':
            param_glue = [{'type': Types.Vec(Types.Text), 'value': items}]
            result = await agent.update_raw_async(canisterId, "glue_push", encode(param_glue))
            if isinstance(result, list) and len(result) > 0 and 'value' in result[0]:
                return result[0]['value']
        return None
    except Exception as e:
        print(f'ICP error: {e}')
        return None


# Funkcja do skracania ID dla wyświetlania
def shorten_id(id_str, start=6, end=6):
    if len(id_str) <= start + end:
        return id_str
    return f"{id_str[:start]}...{id_str[-end:]}"


class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Async Chat")
        self.setStyleSheet("background-color: black; color: white;")
        self.resize(600, 500)

        # Font zmniejszony o 40%
        font_id = QFontDatabase.addApplicationFont("font.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.custom_font = QFont(font_family, int(10 * 0.6))
        else:
            self.custom_font = QFont("Arial", int(10 * 0.6))

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Chat area
        self.chat_area_layout = QVBoxLayout()
        self.chat_area_layout.setSpacing(5)
        self.chat_area_layout.setAlignment(Qt.AlignTop)

        scroll_widget = QWidget()
        scroll_widget.setLayout(self.chat_area_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(scroll_widget)
        self.scroll_area.setStyleSheet("background-color: black;")
        layout.addWidget(self.scroll_area)

        # Input fields
        self.me = ""
        self.sender_label = QLabel("YOU-ID: " + shorten_id(self.me))
        self.sender_label.setFont(self.custom_font)
        layout.addWidget(self.sender_label)

        # kliknięcie w moje ID → kopiowanie do schowka
        self.sender_label.mousePressEvent = self.copy_my_id_to_clipboard

        self.external_sender_input = QLineEdit()
        self.external_sender_input.setPlaceholderText("ID-TARGET")
        self.external_sender_input.setStyleSheet("background-color: black; color: white; border: 1px solid white;")
        self.external_sender_input.setFont(self.custom_font)
        layout.addWidget(self.external_sender_input)

        self.message_input = QTextEdit()
        self.message_input.setFixedHeight(60)
        self.message_input.setStyleSheet("background-color: black; color: white; border: 1px solid white;")
        self.message_input.setFont(self.custom_font)
        layout.addWidget(self.message_input)

        self.send_button = QPushButton("SAY")
        self.send_button.setStyleSheet("background-color: black; color: white; border: 1px solid white; padding: 17px;")
        self.send_button.setFont(self.custom_font)
        self.send_button.clicked.connect(lambda: asyncio.create_task(self.send_message()))
        layout.addWidget(self.send_button)

    def update_me_label(self, new_me):
        self.me = new_me
        self.sender_label.setText("YOU-ID: " + shorten_id(str(self.me)))

    def copy_my_id_to_clipboard(self, event):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.me)
        print(f"[INFO] Skopiowano ID do schowka: {self.me}")

    # Kolor nadawcy
    def get_color_from_text(self, text):
        hash_int = int(hashlib.md5(text.encode()).hexdigest()[:6], 16)
        r = (hash_int >> 16) & 0xFF
        g = (hash_int >> 8) & 0xFF
        b = hash_int & 0xFF
        return f'rgb({r},{g},{b})'

    # ASYNC wysyłanie
    async def send_message(self, sender_override=None, message_override=None):
        sender = sender_override if sender_override else self.external_sender_input.text().strip()
        message = message_override if message_override else self.message_input.toPlainText().strip()
        if not message:
            return
        if(sender == "vms"):
            self._show_message(sender, message, direction="outgoing")
            info = await vms_boot(message)
            self._show_message(sender, info, direction="incoming")
        else:
            value = await icpcon("gluePUSH", ["say", sender, message])
            print(f"[SEND] {sender}: {message}")
            if value != "ok":
                message = "error: " + value

            self._show_message(sender, message, direction="outgoing")
            self.message_input.clear()
            self.external_sender_input.clear()

    # ASYNC odbieranie
    async def receive_message(self, sender, message):
        self._show_message(sender, message, direction="incoming")
        QSound.play("sound.wav")
        print(f"[RECEIVE] {sender}: {message}")

    # Wyświetlanie
    def _show_message(self, sender, message, direction):
        color = self.get_color_from_text(sender)

        frame = QFrame()
        h_layout = QHBoxLayout()
        frame.setLayout(h_layout)

        bubble = QFrame()
        v_layout = QVBoxLayout()
        v_layout.setSpacing(2)
        bubble.setLayout(v_layout)
        bubble.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        max_bubble_width = int(self.width() * 0.9)  # max 70% szerokości okna
        bubble.setMaximumWidth(max_bubble_width)

        if direction == "outgoing":
            bubble.setStyleSheet("background-color: #222; border-radius: 5px; padding: 5px;")
            h_layout.addStretch()
            h_layout.addWidget(bubble)
        else:
            bubble.setStyleSheet("background-color: #444; border-radius: 5px; padding: 5px;")
            h_layout.addWidget(bubble)
            h_layout.addStretch()

        sender_label = QLabel(shorten_id(sender))
        sender_label.setFont(self.custom_font)
        sender_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        sender_label.setWordWrap(True)
        sender_label.mousePressEvent = lambda event, s=sender: self.external_sender_input.setText(s)
        v_layout.addWidget(sender_label)

    # Wiadomość z automatycznym łamaniem nawet długich ciągów
        message_label = QLabel()
        message_label.setFont(self.custom_font)
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # umożliwia kopiowanie
        message_label.setWordWrap(True)
        message_label.setMaximumWidth(max_bubble_width)
        # HTML + word-break: break-all dla bardzo długich ciągów
        message_label.setText(f'<div style="color: {"white" if direction=="outgoing" else "white"}; word-break: break-all;">{message}</div>')

        v_layout.addWidget(message_label)

        self.chat_area_layout.addWidget(frame)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())


# ASYNC BOT LOOP
async def bot_loop(window: ChatApp):
    global vms_repete
    if(vms_repete != ""):
        await window.receive_message("vms", vms_repete)
        vms_repete = ""
    while True:
        await asyncio.sleep(1)
        me_value = await icpcon("glue", ["me"])
        if me_value:
            window.update_me_label(me_value)
        qwery = ["watch"]
        value = await icpcon("glue", qwery)
        if value == "PUSH":
            value = await icpcon("gluePUSH", qwery)
            parts = value.split("--mesage--")
            from_value = parts[0].replace("--from--", "").strip()
            message_value = parts[1].strip()
            await window.receive_message(from_value, message_value)

async def vms_boot(message):
    global canisterId, vms_repete
    if(message == "mlem"):
        return "mlem"
    elif(message == "info"):
        return """VMESSAGER V0.8 - Multi-Canister Messaging Application

This is an application operating within the Voyager ecosystem, where anyone can run their own nodes and set their own rules. 
It represents a new approach to decentralization in the on-chain ecosystem.

Learn more about the Voyager project on GitHub:
https://github.com/tomasz2001/voyager
To see available bot commands, type: help """
    else:
        return "escusme what"

    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    with loop:
        asyncio.ensure_future(bot_loop(window))
        loop.run_forever()
