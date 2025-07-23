# Agent Pydantic na Voyagerze

Ten projekt demonstruje agenta AI zbudowanego w Pythonie, wykorzystującego bibliotekę Pydantic do zarządzania konfiguracją oraz elastyczne mechanizmy integracji z różnymi modelami językowymi (LLM) i narzędziami (w tym niestandardowymi serwerami MCP).

## Funkcjonalności

*   **Wsparcie dla lokalnych modeli LLM:** Integracja z Ollama.
*   **Wsparcie dla zewnętrznych API (OpenAI-compatible):** Możliwość podłączenia dowolnego modelu udostępniającego API zgodne z OpenAI.
*   **Obsługa Narzędzi (Function Calling):** Agent może wywoływać predefiniowane funkcje/narzędzia.
*   **Integracja z MCP:** Wykorzystanie narzędzi MCP (Model Control Program) do interakcji z zewnętrznymi usługami.
*   **Elastyczność MCP:** Możliwość zdefiniowania przez użytkownika własnego, niestandardowego serwera MCP.

## Instalacja

1.  **Sklonuj repozytorium:**
    ```bash
    git clone <adres_repozytorium>
    cd voyager/pydantic-agent
    ```

2.  **Utwórz i aktywuj wirtualne środowisko (zalecane):**
    ```bash
    python -m venv venv
    # Na Windows:
    .\venv\Scripts\activate
    # Na macOS/Linux:
    source venv/bin/activate
    ```

3.  **Zainstaluj zależności:**
    ```bash
    pip install -r requirements.txt
    ```

## Konfiguracja

1.  **Utwórz plik `.env`:**
    Skopiuj plik `.env.example` i zmień jego nazwę na `.env` w katalogu `voyager/pydantic-agent`.
    ```bash
    cp .env.example .env
    ```

2.  **Edytuj plik `.env`:**
    Otwórz plik `.env` w edytorze tekstu i skonfiguruj go zgodnie z Twoimi potrzebami:

    *   **`AGENT_MODE`**: Ustaw na `ollama` lub `openai`, aby wybrać tryb pracy agenta.

    *   **Dla trybu `ollama`:**
        ```dotenv
        OLLAMA_MODEL="llama3" # Nazwa modelu, który masz pobrany lokalnie w Ollama
        ```

    *   **Dla trybu `openai`:**
        ```dotenv
        OPENAI_API_KEY="twoj_klucz_api_openai" # Twój klucz API OpenAI lub kompatybilnego serwera
        OPENAI_BASE_URL="https://api.openai.com/v1" # Opcjonalnie: URL endpointu API (domyślnie OpenAI)
        OPENAI_ORGANIZATION="twoja_organizacja" # Opcjonalnie: ID organizacji OpenAI
        ```

    *   **Opcjonalna konfiguracja serwera MCP:**
        Jeśli chcesz używać własnego serwera MCP, podaj jego URL:
        ```dotenv
        MCP_SERVER_URL="http://localhost:8000/mcp" # Przykładowy URL Twojego serwera MCP
        ```

## Uruchomienie

Upewnij się, że masz aktywne wirtualne środowisko i wszystkie zależności są zainstalowane. Następnie uruchom agenta:

```bash
python main.py
```

Agent uruchomi się i będzie czekał na Twoje zapytania w terminalu. Wpisz `exit`, aby zakończyć działanie agenta.

## Przykładowe Użycie

Po uruchomieniu agenta możesz zadawać mu pytania. Jeśli skonfigurujesz narzędzia ICP i/lub serwer MCP, agent będzie mógł ich używać do odpowiadania na bardziej złożone zapytania.

*   **Pytanie ogólne:** `Powiedz mi coś o Pythonie.`
*   **Pytanie wymagające narzędzia (przykład dla ICP glue_get):** `Pobierz post numer 1 z chan.` (Wymaga odpowiedniego mapowania w narzędziach i działającego kanistra ICP).

## Rozwój

Projekt jest podzielony na moduły:

*   `config.py`: Zarządzanie konfiguracją za pomocą Pydantic.
*   `llm_clients.py`: Implementacja klientów dla Ollama i OpenAI.
*   `tools.py`: Definicje narzędzi i logika wywoływania MCP/ICP.
*   `main.py`: Główna logika agenta, pętla interakcji i orkiestracja.

Zachęcamy do eksplorowania kodu i dostosowywania go do własnych potrzeb.