# V-Messenger

Zdecentralizowany komunikator działający w sieci Internet Computer w ramach ekosystemu VOYAGER.

## Opis

V-Messenger to aplikacja pozwalająca na bezpieczne i anonimowe przesyłanie wiadomości tekstowych pomiędzy użytkownikami (Principal ID) w sieci IC. Aplikacja korzysta z kanistra `vmessage` jako backendu do przechowywania i przekazywania wiadomości.

Projekt zawiera dwie wersje interfejsu użytkownika:
1.  **Aplikacja graficzna (GUI)**: Stworzona w PyQt5, oferuje przyjazny interfejs, automatyczne sprawdzanie wiadomości w tle i łatwe zarządzanie komunikacją.
2.  **Aplikacja konsolowa**: Lekka wersja do obsługi komunikatora z poziomu terminala.

## Kluczowe Funkcje

- **Zdecentralizowana Komunikacja**: Wszystkie wiadomości są przesyłane przez kanister w sieci Internet Computer.
- **Zarządzanie Tożsamością**: Aplikacja automatycznie tworzy i zarządza lokalną tożsamością użytkownika (plik `identity.pem`).
- **Interfejs Graficzny**: Intuicyjna obsługa dzięki GUI opartemu na PyQt5.
- **Automatyczne Odświeżanie**: GUI automatycznie sprawdza nowe wiadomości co 15 sekund.
- **Bezpieczeństwo**: Komunikacja opiera się na Principal ID, zapewniając pseudonimowość.

## Wymagania

- Python 3.x
- Biblioteki Python zawarte w `requirements.txt`:
  - `ic-py`
  - `colorama` (dla wersji konsolowej)
  - `PyQt5`
  - `qasync`

## Instalacja

1. Sklonuj repozytorium lub pobierz pliki projektu.
2. Przejdź do katalogu `vmessager-app`.
3. Zainstaluj wymagane biblioteki:
   ```bash
   pip install -r requirements.txt
   ```

## Uruchomienie

### Wersja Graficzna (GUI)

Aby uruchomić aplikację w wersji graficznej, wykonaj polecenie:
```bash
python maingui.py
```

### Wersja Konsolowa

Aby uruchomić aplikację w trybie konsolowym, wykonaj polecenie:
```bash
python "main copyConsole.py"
```

## Struktura Projektu

- `maingui.py`: Główny plik aplikacji w wersji graficznej (PyQt5).
- `main copyConsole.py`: Główny plik aplikacji w wersji konsolowej.
- `ic_connector.py`: Moduł obsługujący całą logikę komunikacji z kanistrem `vmessage`.
- `identity.pem`: Plik przechowujący Twoją unikalną, lokalną tożsamość w sieci.
- `joystix.otf` / `sound.wav`: Zasoby wykorzystywane przez aplikację GUI.
- `requirements.txt`: Lista zależności projektu.
