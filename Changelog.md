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