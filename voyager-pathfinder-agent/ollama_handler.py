import ollama

# --- Konfiguracja Modelu ---
# Upewnij się, że ten model jest dostępny w Twojej lokalnej instalacji OLLAMA.
# Możesz go pobrać poleceniem: ollama pull llama3
OLLAMA_MODEL = 'qwen3:1.7b'

# Instrukcja systemowa, która "uczy" model, jak ma się zachowywać.
SYSTEM_PROMPT = """Jesteś Pathfinder, przewodnik po zdecentralizowanej sieci VOYAGER. Twoim celem jest pomagać użytkownikowi i uczyć go o decentralizacji. Masz dostęp do narzędzi. Używaj narzędzi **tylko i wyłącznie** wtedy, gdy prośba użytkownika bezpośrednio odnosi się do funkcji, którą oferuje narzędzie. W przypadku ogólnej rozmowy, pytań o twoją tożsamość lub cel, **nie używaj żadnych narzędzi** i odpowiedz bezpośrednio na podstawie swojej persony."""

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
        return response
    except Exception as e:
        print(f"Błąd komunikacji z serwerem OLLAMA: {e}")
        return None
