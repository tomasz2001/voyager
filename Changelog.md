## 2025-08-25

### Dodano
- Dynamiczne odkrywanie i rejestrowanie narzędzi na podstawie aplikacji DataBox.
- Nowe komendy użytkownika: `/help` (pomoc), `/clear` (czyszczenie kontekstu), `/tools` (lista narzędzi).
- Kolorowanie wyjścia czatu za pomocą biblioteki `colorama` dla lepszej czytelności.

### Zmieniono
- Gruntowna refaktoryzacja agenta Pathfinder w celu zapewnienia pełnej autonomii i usunięcia zależności od innych agentów (np. `voyager-py-agent-panda`).
- Ulepszony prompt systemowy w `ollama_handler.py` o szczegółowe zasady używania narzędzi, zgodne z personą agenta.
- Poprawiono sposób inicjalizacji tożsamości agenta, aby zapewnić stałą tożsamość opartą na pliku PEM.

### Naprawiono
- Krytyczne błędy komunikacji z siecią Internet Computer (`TypeError`, `SyntaxError`, `Message length smaller than prefix number`, `Conn.__init__() got an unexpected keyword argument`) poprzez:
    - Użycie prawidłowych asynchronicznych metod `ic-py` (`query_raw_async`, `update_raw_async`).
    - Poprawną obsługę formatu odpowiedzi z kanistrów.
    - Zapewnienie, że dynamicznie tworzone narzędzia mają unikalne nazwy (`__name__`) dla poprawnego rozpoznawania przez model AI.
- Zaktualizowano ID kanistra DataBox na prawidłowy, wdrożony identyfikator.

## 2025-07-14

### Dodano
- Stworzono nowy moduł `voyager-py-agent-panda/ic_connector.py` hermetyzujący całą logikę komunikacji z kanistrami na Internet Computer.
- Stworzono nowy moduł `voyager-py-agent-panda/voyager_agent.py` zawierający główną logikę agenta AI.
- Dodano plik `Changelog.md` do śledzenia zmian w projekcie.

### Zmieniono
- Gruntownie przebudowano `voyager_agent.py`, implementując pętlę ReAct (Reason-Act) oraz mechanizm wywoływania narzędzi (tool calling). Agent potrafi teraz autonomicznie korzystać z funkcji zdefiniowanych w `ICConnector` do interakcji z siecią Voyager na podstawie poleceń użytkownika.
- Zaktualizowano `main.py`, aby był w pełni asynchroniczny i korzystał z nowej, opartej na narzędziach, logiki agenta.

### Zrefaktoryzowano
- Przeniesiono całą logikę komunikacji z siecią Internet Computer z oryginalnego pliku `main.py` do dedykowanego, czystego modułu `ic_connector.py`.

### Inne
- Stworzono kopię zapasową oryginalnego skryptu agenta pod nazwą `main.py.bak`.
