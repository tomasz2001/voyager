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
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from v_chip import chip
from v_medium_newspaper import paper_test, paint_text, np_print
import v_file
import config

# ======================
# ZGODA / DISCLAIMER
# ======================
AGREEMENT_FILE = "user_agreement.accepted"

DISCLAIMER_TEXT = """
§1. Postanowienia ogólne

Niniejsza Umowa Licencyjna Użytkownika Końcowego 
(„EULA”) reguluje zasady korzystania z oprogramowania 
V-Medium-Printer, stanowiącego narzędzie klienckie 
służące do interakcji z rozproszonym ekosystemem VOYAGER, 
działającym w oparciu o infrastrukturę Internet Computer (ICP).

Korzystanie z oprogramowania oznacza pełną 
akceptację wszystkich postanowień niniejszej EULA. 
W przypadku braku zgody użytkownik zobowiązany 
jest do zaprzestania korzystania z oprogramowania.

§2. Charakter i zamysł ekosystemu VOYAGER

Ekosystem VOYAGER został zaprojektowany jako 
zdecentralizowana infrastruktura technologiczna, 
której celem jest umożliwienie użytkownikom 
oraz autonomicznym agentom programowym odkrywania usług, 
komunikacji oraz wymiany danych w sposób:

otwarty,

odporny na cenzurę,

niezależny od centralnych podmiotów kontrolnych.

VOYAGER nie jest systemem redakcyjnym, wydawniczym ani moderacyjnym. 
Nie pełni funkcji nadzoru nad treściami, nie dokonuje ich oceny ani selekcji, 
a jedynie udostępnia mechanizmy techniczne umożliwiające ich przetwarzanie.

§3. Agent, Voyager App i architektura systemu
1. Agent

Agent jest aplikacją działającą lokalnie 
po stronie użytkownika lub jako usługa, 
której zadaniem jest techniczna interakcja z 
ekosystemem VOYAGER. Agent może przyjmować różne formy, 
w tym narzędzi komunikacyjnych, interfejsów 
użytkownika lub agentów autonomicznych.

Agent nie posiada uprawnień redakcyjnych ani 
decyzyjnych w odniesieniu do treści, które przetwarza.

2. Voyager App

Voyager App jest niezależną aplikacją działającą 
jako canister w sieci Internet Computer (ICP). 
Każdy użytkownik ma możliwość uruchomienia własnej 
instancji aplikacji, jej modyfikacji oraz rozwoju, 
z zachowaniem kompatybilności z ekosystemem.

Voyager Apps funkcjonują w modelu:

decentralizacji,

równości uczestników,

braku centralnego punktu kontroli.

3. Voyager-DataBox

Voyager-DataBox stanowi zdecentralizowany 
katalog usług, który przechowuje 
informacje o aplikacjach oraz innych DataBoxach. 
Wzajemne referencjonowanie DataBoxów 
tworzy rozproszoną sieć odkrywania 
usług, opartą na zaufaniu i decyzjach użytkowników.

§4. Brak kontroli i odpowiedzialności za treści

Użytkownik przyjmuje do wiadomości, że:

Treści dostępne w ekosystemie VOYAGER 
pochodzą od niezależnych podmiotów.

Twórcy V-Medium-Printer oraz osoby związane 
z ekosystemem VOYAGER nie mają faktycznej 
ani prawnej możliwości sprawowania 
kontroli nad tymi treściami.

Oprogramowanie nie dokonuje weryfikacji 
prawdziwości, legalności ani rzetelności danych.

Wszelka odpowiedzialność za treści, 
w tym za ich akceptację, publikację, druk lub dalsze 
rozpowszechnianie, spoczywa wyłącznie na użytkowniku.

§5. Obowiązki użytkownika („drukarza”)

Ze względu na zdecentralizowaną naturę 
systemu, użytkownik zobowiązuje się do:

samodzielnej i skrupulatnej 
weryfikacji treści przed ich akceptacją,

przeciwdziałania rozpowszechnianiu dezinformacji,

korzystania z oprogramowania zgodnie 
z obowiązującym prawem i zasadami etycznymi.

Użytkownik przyjmuje do wiadomości, że możliwości 
scentralizowanego reagowania na nadużycia będą 
ulegały dalszemu ograniczeniu wraz z rozwojem ekosystemu.

§6. Reklamy i treści sponsorowane

Dostawcy węzłów, operatorzy canistrów oraz podmioty 
uczestniczące w ekosystemie VOYAGER zastrzegają 
sobie prawo do umieszczania treści reklamowych,
informacyjnych lub sponsorowanych w danych źródłowych, 
makietach lub szablonach.

Twórcy V-Medium-Printer nie ponoszą odpowiedzialności 
za treść takich materiałów ani nie przyjmują 
roszczeń związanych z ich obecnością.

§7. Brak odpowiedzialności twórców

Twórcy V-Medium-Printer nie inicjują, nie redagują, 
nie zatwierdzają ani nie autoryzują treści przetwarzanych 
przez oprogramowanie. Udostępnienie narzędzia technicznego 
nie oznacza aprobaty ani współodpowiedzialności 
za sposób jego wykorzystania.

§8. Informacje licencyjne i projektowe

Project Name: VOYAGER
License: GNU AGPLv3
Public Chat: https://t.me/voyager_system

Korzystanie z oprogramowania oznacza akceptację 
zdecentralizowanego charakteru ekosystemu VOYAGER 
oraz wynikających z niego ograniczeń.

§9. Postanowienia końcowe

Oprogramowanie udostępniane jest „as-is”. W najszerszym 
dopuszczalnym przez prawo zakresie twórcy wyłączają 
swoją odpowiedzialność za szkody bezpośrednie, 
pośrednie, wtórne lub wynikowe.
"""

# ======================
# WYGLĄD
# ======================
Window.clearcolor = (0, 0, 0, 1)

GREEN_BG = (0, 0.78, 0.33, 1)
GREEN_TEXT = (1, 1, 1, 1)
DARK_BG = (0.15, 0.15, 0.15, 1)
WHITE = (1, 1, 1, 1)

REGISTERS_COUNT = 32
TEMPLATE_PIN_INDEX = 0
TEMPLATE_NAME = "v_medium.png"

# ======================
# POPUP ZGODY
# ======================
class AgreementPopup(Popup):
    def __init__(self, on_accept, **kwargs):
        super().__init__(**kwargs)
        self.title = "Warunki korzystania – V-Medium"
        self.size_hint = (0.9, 0.9)
        self.auto_dismiss = False

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        scroll = ScrollView()
        label = Label(
            text=DISCLAIMER_TEXT,
            size_hint_y=None,
            color=WHITE,
            halign="left",
            valign="top"
        )
        label.bind(texture_size=label.setter("size"))
        scroll.add_widget(label)

        buttons = BoxLayout(size_hint_y=None, height=50, spacing=10)

        accept = Button(
            text="Zgadzam się",
            background_color=GREEN_BG,
            color=GREEN_TEXT
        )
        reject = Button(
            text="Nie zgadzam się",
            background_color=(0.4, 0, 0, 1),
            color=WHITE
        )

        accept.bind(on_press=lambda *_: self.accept(on_accept))
        reject.bind(on_press=lambda *_: App.get_running_app().stop())

        buttons.add_widget(accept)
        buttons.add_widget(reject)

        layout.add_widget(scroll)
        layout.add_widget(buttons)

        self.content = layout

    def accept(self, callback):
        with open(AGREEMENT_FILE, "w", encoding="utf-8") as f:
            f.write("accepted")
        self.dismiss()
        callback()

# ======================
# GŁÓWNY GUI
# ======================
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
            color=GREEN_TEXT
        )
        self.start_btn.bind(on_press=self.start_scan)
        self.add_widget(self.start_btn)

        # ======================
        # STATUS
        # ======================
        self.status = self.make_label("Status: gotowy")
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
        # PRZYCISKI
        # ======================
        buttons = BoxLayout(size_hint_y=None, height=50, spacing=10)

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

        buttons.add_widget(self.accept_btn)
        buttons.add_widget(self.reject_btn)
        buttons.add_widget(self.print_btn)

        self.add_widget(buttons)

        # ======================
        # DRUK OSTATNIEGO WYDANIA
        # ======================
        self.print_last_button = Button(
            text="Wydrukuj nowe wydanie",
            size_hint_y=None,
            height=50,
            background_color=(0.0, 0.6, 0.8, 1),
            color=WHITE,
            disabled=True
        )
        self.print_last_button.opacity = 0
        self.print_last_button.bind(on_press=self.print_last_newspaper)
        self.add_widget(self.print_last_button)

        # ======================
        # STAN
        # ======================
        self.canister = None
        self.news_queue = []
        self.current_news = None
        self.last_newspaper_ready = False

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
    # TEMPLATE
    # ======================
    async def fetch_fresh_template(self):
        try:
            if os.path.exists(TEMPLATE_NAME):
                os.remove(TEMPLATE_NAME)
            await v_file.download_file(
                canister_id=self.canister,
                pin_index=TEMPLATE_PIN_INDEX,
                save_dir="."
            )
        except Exception as e:
            Clock.schedule_once(
                lambda *_: self.set_status(f"Błąd pobierania makiety: {e}")
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

        self.status.text = "Pobieranie makiety..."
        threading.Thread(
            target=lambda: asyncio.run(self.pipeline()),
            daemon=True
        ).start()

    async def pipeline(self):
        await self.fetch_fresh_template()
        Clock.schedule_once(lambda *_: self.set_status("Skanowanie rejestrów..."))
        await self.scan_registers()

    def set_status(self, text):
        self.status.text = text

    # ======================
    # SKAN
    # ======================
    async def scan_registers(self):
        REGISTERS_COUNT = int(await chip("size", self.canister))
        for i in range(REGISTERS_COUNT):
            try:
                text = await chip(str(i), self.canister)
                if text and text.strip():
                    self.news_queue.append(text)
            except Exception:
                continue
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
    # DRUK
    # ======================
    def print_current(self, *_):
        if self.text_left or self.text_right:
            try:
                self.build_newspaper()
                np_print()
                self.status.text = "Bieżąca wersja wydrukowana"
            except Exception:
                self.status.text = "Drukarka niedostępna"
        else:
            self.status.text = "Brak treści do wydrukowania"

    def print_last_newspaper(self, *_):
        if not self.last_newspaper_ready:
            self.status.text = "Brak gotowej gazety do druku"
            return
        try:
            np_print()
            self.status.text = "Ostatnie wydanie wydrukowane"
        except Exception:
            self.status.text = "Drukarka niedostępna"

    # ======================
    # KONIEC
    # ======================
    def finish(self):
        self.status.text = "Składanie gazety..."
        self.news_box.text = ""

        try:
            self.build_newspaper()
            self.last_newspaper_ready = True

            self.print_last_button.opacity = 1
            self.print_last_button.disabled = False

            if config.AUTO_PRINT:
                try:
                    np_print()
                    self.status.text = "Gazeta wydrukowana"
                except Exception:
                    self.status.text = "Drukarka niedostępna"
            else:
                self.status.text = "Gotowe (bez auto-druku)"
        except Exception as e:
            self.status.text = f"Błąd składania gazety: {e}"

# ======================
# APP
# ======================
class V_mediumApp(App):
    def build(self):
        if not os.path.exists(AGREEMENT_FILE):
            self.root_box = BoxLayout()
            Clock.schedule_once(self.show_agreement, 0)
            return self.root_box
        return WalesaGUI()

    def show_agreement(self, *_):
        AgreementPopup(self.start_app).open()

    def start_app(self):
        self.root_box.clear_widgets()
        self.root_box.add_widget(WalesaGUI())

if __name__ == "__main__":
    V_mediumApp().run()
