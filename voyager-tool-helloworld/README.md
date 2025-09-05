# Voyager Helloworld Tool

## Wprowadzenie

**Voyager Helloworld Tool** to prosty kanister działający w sieci Internet Computer (IC), stworzony jako podstawowy przykład narzędzia w ekosystemie VOYAGER. Jego głównym celem jest weryfikacja podstawowej komunikacji między agentem AI a kanistrem w sieci IC.

## Funkcjonalność

Kanister udostępnia jedną, prostą funkcję:

### 1. `hello()`
*   **Cel:** Zwraca stały tekst, potwierdzając, że kanister działa i odpowiada na wywołania.
*   **Opis:** Funkcja ta nie przyjmuje żadnych argumentów i zawsze zwraca ten sam tekst: "narzędzie działa". Jest to idealne do szybkiego testowania połączenia i działania narzędzi.
*   **Zwraca:** `Text` - tekst "narzędzie działa".

## Kod Motoko (Fragment)

```motoko
actor {
  public query func hello() : async Text {
    return "narzędzie działa";
  };
}
```

## Wdrożenie

Aby wdrożyć kanister `voyager-tool-helloworld` w sieci Internet Computer (lokalnie lub w sieci głównej), użyj narzędzia `dfx`:

1.  Przejdź do katalogu projektu `voyager-tool-helloworld`.
2.  Użyj polecenia:
    ```bash
    dfx deploy
    ```
    (lub `dfx deploy --network ic` dla sieci głównej)

## Integracja z Agentem Pathfinder

Agent AI Pathfinder wykorzystuje ten kanister do implementacji narzędzia `helloworld_tool`, które jest używane do początkowych testów komunikacji i działania agenta.