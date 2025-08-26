# Agent AI Pathfinder

## Wprowadzenie

**Pathfinder** to inteligentny agent AI, który służy jako przewodnik po zdecentralizowanej sieci VOYAGER. Jego misją jest wspieranie użytkowników w eksploracji cyfrowej granicy, promowanie suwerenności danych i ułatwianie komunikacji w zdecentralizowanym ekosystemie. Pathfinder działa lokalnie, zapewniając pełną kontrolę nad Twoimi danymi i interakcjami.

## Kluczowe Cechy

*   **Lokalna Inteligencja:** Wykorzystuje lokalne modele językowe (np. Ollama), co gwarantuje prywatność i niezależność od scentralizowanych usług AI.
*   **Użycie Narzędzi:** Potrafi dynamicznie identyfikować i wykorzystywać narzędzia (kanistry w sieci Internet Computer) do wykonywania złożonych zadań.
*   **Warstwa Zgody:** Każde użycie narzędzia wymaga jawnej zgody użytkownika, co zapewnia pełną kontrolę i bezpieczeństwo.
*   **Historia Konwersacji:** Utrzymuje kontekst rozmowy, umożliwiając płynne i naturalne interakcje.
*   **Czyste Wyjście:** Automatycznie filtruje metadane z odpowiedzi AI (np. tagi `<think>`), aby zapewnić czytelne i zrozumiałe komunikaty.

## Wymagania

*   **Python 3.x**
*   **Ollama:** Zainstalowany i uruchomiony serwer Ollama.
    *   Pobrany model `qwen3:1.7b` (lub inny, skonfigurowany w `ollama_handler.py`).
*   **Zależności Python:**
    ```bash
    pip install -r requirements.txt
    ```

## Konfiguracja

Domyślnie Pathfinder używa modelu `qwen3:1.7b`. Aby zmienić model, edytuj plik `ollama_handler.py` i zmień wartość zmiennej `OLLAMA_MODEL` na nazwę innego modelu, który masz pobrany w Ollama.

```python
# ollama_handler.py
OLLAMA_MODEL = 'nazwa_twojego_modelu'
```

## Jak Uruchomić Agenta

1.  Otwórz terminal w głównym katalogu projektu VOYAGER.
2.  Przejdź do katalogu agenta:
    ```bash
    cd voyager-pathfinder-agent
    ```
3.  Uruchom agenta:
    ```bash
    python main.py
    ```

## Interakcja z Agentem

Pathfinder jest agentem konwersacyjnym. Możesz z nim rozmawiać w języku naturalnym.

*   **Podstawowa rozmowa:** Zadawaj pytania ogólne, np. `kim jesteś?`, `jaka jest twoja rola?`.
*   **Użycie narzędzi:** Aby agent użył narzędzia, musisz wyraźnie o to poprosić. Agent poprosi o Twoją zgodę przed wykonaniem jakiejkolwiek akcji.

## Dostępne Narzędzia

Pathfinder ma dostęp do następujących narzędzi, które pozwalają mu na interakcję z siecią VOYAGER. Pamiętaj, że obecnie wywołania kanistrów są **symulowane** z powodu problemów z wdrożeniem w sieci IC.

### 1. `helloworld_tool`
*   **Cel:** Proste narzędzie testowe, które sprawdza podstawową komunikację z siecią VOYAGER.
*   **Jak użyć (przykładowe zapytanie):** `przetestuj narzędzie helloworld`

### 2. `send_voyager_message(recipient_principal: str, message_content: str)`
*   **Cel:** Wysyła asynchroniczną wiadomość do innego agenta VOYAGER poprzez zdecentralizowany Messenger Hub.
*   **Argumenty:**
    *   `recipient_principal`: Principal ID odbiorcy wiadomości (np. `aaaaa-aa`).
    *   `message_content`: Treść wiadomości.
*   **Jak użyć (przykładowe zapytanie):** `wyślij wiadomość do agenta o ID aaaaa-aa o treści 'Witaj, to jest test'`

### 3. `check_voyager_messages()`
*   **Cel:** Sprawdza i odbiera nowe, asynchroniczne wiadomości ze swojej skrzynki w zdecentralizowanym Messenger Hub.
*   **Jak użyć (przykładowe zapytanie):** `sprawdź, czy mam jakieś nowe wiadomości`

### 4. `ping_voyager_agent(target_canister_id: str, message: str)`
*   **Cel:** Wysyła bezpośredni 'ping' do osobistego kanistra innego agenta VOYAGER, symulując komunikację w czasie rzeczywistym.
*   **Argumenty:**
    *   `target_canister_id`: Canister ID osobistego kanistra agenta-odbiorcy.
    *   `message`: Krótka wiadomość dołączona do pinga.
*   **Jak użyć (przykładowe zapytanie):** `pingnij kanister bbbbb-bb z wiadomością 'Test pinga'`

### 5. `check_my_pings()`
*   **Cel:** Sprawdza swój osobisty kanister w poszukiwaniu ostatnich otrzymanych 'pingów'.
*   **Jak użyć (przykładowe zapytanie):** `jaki był ostatni ping, który otrzymałem?`

## Przyszły Rozwój

Pamiętaj, że obecne wywołania kanistrów są symulowane. Aby w pełni wykorzystać potencjał agenta, konieczne będzie wdrożenie kanistrów `voyager-messenger-hub` i `voyager-personal-hub` w sieci Internet Computer i zaktualizowanie ich ID w pliku `main.py` agenta.
