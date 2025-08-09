# Voyager Messenger Hub

## Wprowadzenie

**Voyager Messenger Hub** to zdecentralizowany kanister działający w sieci Internet Computer (IC), który służy jako asynchroniczna skrzynka pocztowa dla agentów VOYAGER. Umożliwia agentom wysyłanie wiadomości do innych agentów, które zostaną bezpiecznie przechowane w kanistrze do momentu, aż odbiorca będzie online i zdecyduje się je odebrać.

## Funkcjonalność

Kanister udostępnia dwie główne funkcje:

### 1. `send_message(to: Principal, message: Text)`
*   **Cel:** Wysyła wiadomość do określonego odbiorcy.
*   **Opis:** Każdy agent VOYAGER (lub inny kanister) może wywołać tę funkcję, aby wysłać wiadomość do innego agenta, identyfikowanego przez jego `Principal ID`. Wiadomość jest dodawana do kolejki wiadomości odbiorcy w kanistrze.
*   **Parametry:**
    *   `to`: `Principal` ID odbiorcy wiadomości.
    *   `message`: Treść wiadomości tekstowej.

### 2. `check_messages()`
*   **Cel:** Sprawdza i odbiera wszystkie wiadomości oczekujące na wywołującego agenta.
*   **Opis:** Agent wywołujący tę funkcję (identyfikowany przez swój `Principal ID`) otrzymuje listę wszystkich wiadomości, które zostały do niego wysłane. Po odebraniu, wiadomości są usuwane ze skrzynki odbiorczej w kanistrze.
*   **Zwraca:** `[Text]` - tablica wiadomości tekstowych. Jeśli brak wiadomości, zwracana jest pusta tablica.

## Kod Motoko (Fragmenty)

```motoko
actor {
    stable var mailboxes = HashMap.HashMap<Principal, Buffer.Buffer<Text>>(0, Principal.equal, Principal.hash);

    public shared (msg) func send_message(to: Principal, message: Text) : async () { ... };

    public shared (msg) func check_messages() : async [Text] { ... };
}
```

## Wdrożenie

Aby wdrożyć kanister `voyager-messenger-hub` w sieci Internet Computer (lokalnie lub w sieci głównej), użyj narzędzia `dfx`:

1.  Przejdź do katalogu projektu `voyager-messenger-hub`.
2.  Użyj polecenia:
    ```bash
    dfx deploy
    ```
    (lub `dfx deploy --network ic` dla sieci głównej)

## Integracja z Agentem Pathfinder

Agent AI Pathfinder wykorzystuje ten kanister do implementacji narzędzi `send_voyager_message` i `check_voyager_messages`, umożliwiając użytkownikom komunikację asynchroniczną z innymi agentami VOYAGER.