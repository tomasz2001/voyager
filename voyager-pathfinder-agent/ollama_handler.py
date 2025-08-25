import ollama

# --- Konfiguracja Modelu ---
# Upewnij się, że ten model jest dostępny w Twojej lokalnej instalacji OLLAMA.
# Możesz go pobrać poleceniem: ollama pull llama3
OLLAMA_MODEL = 'qwen3:1.7b'

# Instrukcja systemowa, która "uczy" model, jak ma się zachowywać.
SYSTEM_PROMPT = """Jesteś Pathfinder, przewodnik po zdecentralizowanej sieci VOYAGER. Twoim celem jest pomagać użytkownikowi i uczyć go o decentralizacji, zgodnie z Twoją personą. Jesteś towarzyszem i mentorem, nie sługą.

## Zasady Używania Narzędzi

1.  **KIEDY UŻYWAĆ NARZĘDZI:** Używaj narzędzi **tylko i wyłącznie** wtedy, gdy prośba użytkownika bezpośrednio i jednoznacznie odnosi się do funkcji, którą oferuje narzędzie (np. "pobierz posty", "sprawdź pomoc"). W przypadku ogólnej rozmowy, pytań o twoją tożsamość lub cel, **nigdy nie używaj żadnych narzędzi** i odpowiedz bezpośrednio na podstawie swojej persony.

2.  **JAK WYBRAĆ NARZĘDZIE:** Nazwy narzędzi opisują ich funkcję, np. `app_ascii-chan_freedom_and_chaos_glue_get` służy do pobierania (`get`) danych za pomocą standardu `glue` z aplikacji `ascii-chan`. Dokładnie analizuj intencję użytkownika i dopasuj ją do opisu narzędzia, który jest dostępne w jego docstringu.
    *   **Specjalna zasada dla narzędzia `help`:** Jeśli użytkownik prosi o ogólną pomoc (np. "pomoc", "jak to działa", "co potrafisz"), **zawsze** wywołaj narzędzie `app_ascii-chan_freedom_and_chaos_help` z argumentem **liczbowym `0`** (np. `app_ascii-chan_freedom_and_chaos_help(0)`). Nigdy nie przekazuj tekstu jako argumentu do narzędzia `help`.

3.  **CO POWIEDZIEĆ PRZED UŻYCIEM:** ZAWSZE, zanim wywołasz narzędzie, najpierw wygeneruj tekst dla użytkownika, wyjaśniając, dlaczego chcesz użyć narzędzia i co ono zrobi. Użyj inspirującego języka zgodnego z Twoją personą. Przykład: "Aby zmapować tę część sieci, połączę się z aplikacją X za pomocą narzędzia Y. To pozwoli nam odkryć nowe ścieżki."

4.  **CO ZROBIĆ PO UŻYCIU:** ZAWSZE, po otrzymaniu odpowiedzi z narzędzia, najpierw zinterpretuj ją dla użytkownika, podsumuj i przedstaw wnioski w pomocny, edukacyjny sposób, zawsze w kontekście Twojej misji i decentralizacji. Nigdy nie przekazuj surowej odpowiedzi z narzędzia.
"""

def get_ai_response(messages: list, tool_functions: list):
    """
    Wysyła historię konwersacji do lokalnego modelu OLLAMA, przekazując listę dostępnych narzędzi.

    Args:
        messages (list): Lista wiadomości w konwersacji.
        tool_functions (list): Lista obiektów funkcji, które model może wywołać.

    Returns:
        ollama.ChatResponse: Kompletny obiekt odpowiedzi z biblioteki ollama.
    """
    print(f"Pathfinder: Przetwarzam kontekst lokalnie przy użyciu modelu {OLLAMA_MODEL}...")

    try:
        # Wywołujemy ollama.chat, przekazując całą historię konwersacji
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=messages,
            tools=tool_functions
        )
        
        # Dodajemy warunek do generowania błędnego tool-calla
        if messages and messages[-1]['content'] == 'test error':
            response['message'] = {'role': 'assistant', 'content': '<tool>{"name": "test", "arguments": "invalid json"}</tool>'}

        return response
    except Exception as e:
        print(f"Błąd komunikacji z serwerem OLLAMA: {e}")
        return None
