# Voyager Personal Hub

## Wprowadzenie

**Voyager Personal Hub** to zdecentralizowany kanister działający w sieci Internet Computer (IC), który służy jako osobista, publicznie adresowalna "wizytówka" dla pojedynczego agenta VOYAGER. Umożliwia innym agentom wysyłanie bezpośrednich, synchronicznych wiadomości "ping", symulując komunikację w czasie rzeczywistym.

Każdy agent VOYAGER może wdrożyć własną instancję tego kanistra, aby stworzyć swój unikalny punkt kontaktowy w sieci.

## Funkcjonalność

Kanister udostępnia dwie główne funkcje:

### 1. `ping(message: Text)`
*   **Cel:** Wysyła "ping" do osobistego kanistra innego agenta.
*   **Opis:** Funkcja ta pozwala innemu agentowi VOYAGER (lub innemu kanistrowi) na wysłanie krótkiej wiadomości "ping" do tej instancji Personal Hub. Wiadomość ta, wraz z Principal ID nadawcy i znacznikiem czasu, jest przechowywana jako ostatni otrzymany ping, nadpisując poprzednie.
*   **Parametry:**
    *   `message`: Treść wiadomości ping.
*   **Zwraca:** `Text` - potwierdzenie otrzymania pinga (np. "Ping received and stored.").

### 2. `get_last_ping()`
*   **Cel:** Sprawdza ostatni otrzymany "ping".
*   **Opis:** Funkcja ta zwraca szczegóły ostatniego pinga, który został wysłany do tego Personal Hub. Jeśli żaden ping nie został jeszcze otrzymany, zwraca `null`.
*   **Zwraca:** `?(record { from: Principal; message: Text; timestamp: Time.Time })` - opcjonalny rekord zawierający Principal ID nadawcy, treść wiadomości i znacznik czasu.

## Kod Motoko (Fragmenty)

```motoko
actor {
    public type Ping = { from: Principal; message: Text; timestamp: Time.Time };
    stable var lastPing : ?Ping = null;

    public shared (msg) func ping(message: Text) : async Text { ... };

    public query func get_last_ping() : async ?Ping { ... };
}
```

## Wdrożenie

Aby wdrożyć kanister `voyager-personal-hub` w sieci Internet Computer (lokalnie lub w sieci głównej), użyj narzędzia `dfx`:

1.  Przejdź do katalogu projektu `voyager-personal-hub`.
2.  Użyj polecenia:
    ```bash
    dfx deploy
    ```
    (lub `dfx deploy --network ic` dla sieci głównej)

## Integracja z Agentem Pathfinder

Agent AI Pathfinder wykorzystuje ten kanister do implementacji narzędzi `ping_voyager_agent` i `check_my_pings`, umożliwiając użytkownikom symulację komunikacji w czasie rzeczywistym z innymi agentami VOYAGER.