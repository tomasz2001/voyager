import asyncio
import threading
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from v_chip import chip
from v_medium_newspaper import paper_test, paint_text, np_print
import v_file
import config

# ======================
# WYGLĄD
# ======================
Window.clearcolor = (0, 0, 0, 1)  # czarne tło

# Kolory – poprawione: biały tekst na zielonym, nie czarny!
GREEN_BG = (0, 0.78, 0.33, 1)    # zielone tło przycisków
GREEN_TEXT = (1, 1, 1, 1)        # biały tekst na zielonym
DARK_BG = (0.15, 0.15, 0.15, 1)
WHITE = (1, 1, 1, 1)

REGISTERS_COUNT = 32
TEMPLATE_PIN_INDEX = 0
TEMPLATE_NAME = "v_medium.png"

class WalesaGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=12,
            spacing=10,
            **kwargs
        )
        self.text_left = ""
        self.text_right = ""

        # ======================
        # CANISTER
        # ======================
        self.add_widget(self.make_label("Canister / Węzeł IC"))
        self.canister_input = TextInput(
            text=config.DEFAULT_CANISTER,
            multiline=False,
            size_hint_y=None,
            height=40,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=WHITE,
            cursor_color=GREEN_BG
        )
        self.add_widget(self.canister_input)

        self.start_btn = Button(
            text="Start – sprawdź istniejące newsy",
            size_hint_y=None,
            height=45,
            background_color=GREEN_BG,
            color=GREEN_TEXT  # biały tekst!
        )
        self.start_btn.bind(on_press=self.start_scan)
        self.add_widget(self.start_btn)

        # ======================
        # STATUS
        # ======================
        self.status = self.make_label("Status: gotowy")
        self.status.color = WHITE
        self.add_widget(self.status)

        # ======================
        # NEWS
        # ======================
        self.news_box = TextInput(
            readonly=True,
            background_color=(0.05, 0.05, 0.05, 1),
            foreground_color=WHITE
        )
        self.add_widget(self.news_box)

        # ======================
        # PRZYCISKI GŁÓWNE
        # ======================
        btns = BoxLayout(size_hint_y=None, height=50, spacing=10)

        self.accept_btn = Button(
            text="Akceptuj",
            background_color=GREEN_BG,
            color=GREEN_TEXT
        )
        self.reject_btn = Button(
            text="Odrzuć",
            background_color=DARK_BG,
            color=WHITE
        )
        self.print_btn = Button(
            text="Drukuj ostatnią",
            background_color=(0.1, 0.5, 0.1, 1),
            color=WHITE
        )

        self.accept_btn.bind(on_press=self.accept_current)
        self.reject_btn.bind(on_press=self.reject_current)
        self.print_btn.bind(on_press=self.print_current)

        btns.add_widget(self.accept_btn)
        btns.add_widget(self.reject_btn)
        btns.add_widget(self.print_btn)
        self.add_widget(btns)

        # ======================
        # NOWY PRZYCISK – DRUK OSTATNIEGO WYDANIA
        # ======================
        self.print_last_button = Button(
            text="Wydrukuj nowe wydanie",
            size_hint_y=None,
            height=50,
            background_color=(0.0, 0.6, 0.8, 1),  # niebiesko-zielony, żeby się wyróżniał
            color=WHITE,
            disabled=False
        )
        self.print_last_button.opacity = 0     # ukryty na start
        self.print_last_button.disabled = True
        self.print_last_button.bind(on_press=self.print_last_newspaper)
        self.add_widget(self.print_last_button)

        # ======================
        # STAN
        # ======================
        self.canister = None
        self.news_queue = []
        self.current_news = None
        self.last_newspaper_ready = False  # flaga: czy mamy gotową gazetę

    # ======================
    # UI helpers
    # ======================
    def make_label(self, text):
        return Label(
            text=text,
            color=WHITE,
            size_hint_y=None,
            height=30
        )

    # ======================
    # LOGIKA GAZETY
    # ======================
    def can_accept(self, text):
        return paper_test(text, self.text_left, self.text_right) in ("1_ok", "2_ok")

    def accept_text(self, text):
        test = paper_test(text, self.text_left, self.text_right)
        if test == "1_ok":
            self.text_left += ("[endend]" if self.text_left else "") + text
            return True
        if test == "2_ok":
            self.text_right += ("[endend]" if self.text_right else "") + text
            return True
        return False

    def is_full(self):
        return not self.can_accept("TEST")

    def build_newspaper(self):
        paint_text(self.text_left, self.text_right)

    # ======================
    # TEMPLATE – AUTO
    # ======================
    async def fetch_fresh_template(self):
        if os.path.exists(TEMPLATE_NAME):
            os.remove(TEMPLATE_NAME)
        await v_file.download_file(
            canister_id=self.canister,
            pin_index=TEMPLATE_PIN_INDEX,
            save_dir="."
        )

    # ======================
    # START
    # ======================
    def start_scan(self, *_):
        self.text_left = ""
        self.text_right = ""
        self.canister = self.canister_input.text.strip()
        if not self.canister:
            self.status.text = "Brak canister ID"
            return

        self.status.text = "Pobieranie makiety…"
        threading.Thread(
            target=lambda: asyncio.run(self.pipeline()),
            daemon=True
        ).start()

    async def pipeline(self):
        try:
            await self.fetch_fresh_template()
            Clock.schedule_once(lambda *_: self.set_status("Skanowanie 32 rejestrów…"))
            await self.scan_registers()
        except Exception as e:
            Clock.schedule_once(lambda *_: self.set_status(f"Błąd: {e}"))

    def set_status(self, txt):
        self.status.text = txt

    # ======================
    # ASYNC – SKAN
    # ======================
    async def scan_registers(self):
        for i in range(REGISTERS_COUNT):
            try:
                text = await chip(str(i), self.canister)
            except Exception:
                continue
            if text and text.strip():
                self.news_queue.append(text)
        Clock.schedule_once(lambda *_: self.show_next_news())

    # ======================
    # FLOW NEWSÓW
    # ======================
    def show_next_news(self):
        if not self.news_queue or self.is_full():
            self.finish()
            return
        self.current_news = self.news_queue.pop(0)
        self.news_box.text = self.current_news
        self.status.text = "Artykuł do decyzji"

    def accept_current(self, *_):
        if self.current_news and self.can_accept(self.current_news):
            self.accept_text(self.current_news)
            self.show_next_news()

    def reject_current(self, *_):
        self.show_next_news()

    # ======================
    # DRUKOWANIE – BIEŻĄCE (w trakcie)
    # ======================
    def print_current(self, *_):
        if self.text_left or self.text_right:
            try:
                self.build_newspaper()
                np_print()
                self.status.text = "🖨️ Bieżąca wersja wydrukowana"
            except Exception:
                self.status.text = "⚠️ Drukarka niedostępna"
        else:
            self.status.text = "⚠️ Brak treści do wydrukowania"

    # ======================
    # NOWA FUNKCJA – DRUK OSTATNIEGO WYDANIA
    # ======================
    def print_last_newspaper(self, *_):
        if not self.last_newspaper_ready:
            self.status.text = "⚠️ Brak gotowej gazety do druku"
            return
        try:
            np_print()  # drukuje ostatnią wygenerowaną gazetę
            self.status.text = "🖨️ Ostatnie wydanie wydrukowane"
        except Exception:
            self.status.text = "⚠️ Drukarka niedostępna"

    # ======================
    # KONIEC + DRUK – ZMIENIONE
    # ======================
    def finish(self):
        self.status.text = "📄 Składanie gazety…"
        self.news_box.text = ""
        self.build_newspaper()

        # Oznaczamy, że gazeta jest gotowa
        self.last_newspaper_ready = True

        # Pokazujemy przycisk do wielokrotnego druku
        self.print_last_button.opacity = 1
        self.print_last_button.disabled = False

        if config.AUTO_PRINT:
            try:
                np_print()
                self.status.text = "🖨️ Gazeta wydrukowana"
            except Exception:
                self.status.text = "⚠️ Drukarka niedostępna"
        else:
            self.status.text = "✔️ Gotowe (bez auto-druku)"

        # NIC NIE WYŁĄCZAMY – wszystkie przyciski aktywne!

class V_mediumApp(App):
    def build(self):
        return WalesaGUI()

if __name__ == "__main__":
    V_mediumApp().run()