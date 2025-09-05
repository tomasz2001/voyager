import Principal "mo:base/Principal";
import Time "mo:base/Time";

/**
 * Kanister VOYAGER Personal Hub
 * Działa jak osobista, publicznie adresowalna "wizytówka" dla pojedynczego agenta VOYAGER.
 * Umożliwia innym agentom wysyłanie bezpośrednich, synchronicznych wiadomości "ping".
 */
actor {

    // Definiujemy strukturę danych dla pojedynczego pinga.
    public type Ping = {
        from: Principal;
        message: Text;
        timestamp: Time.Time;
    };

    // Używamy stabilnej pamięci, aby ostatni ping przetrwał aktualizacje kanistra.
    // Znak '?' oznacza, że wartość jest opcjonalna (może być `null`, jeśli nikt jeszcze nie wysłał pinga).
    stable var lastPing : ?Ping = null;

    /**
     * Publiczna funkcja, którą inne agenty mogą wywołać, aby wysłać "ping".
     * Zapisuje informacje o pingu, nadpisując poprzedni.
     * @param message - Treść wiadomości w pingu.
     * @return - Zwraca tekstowe potwierdzenie otrzymania pinga.
     */
    public shared (msg) func ping(message: Text) : async Text {
        let caller = msg.caller;
        lastPing := ?{
            from = caller;
            message = message;
            timestamp = Time.now();
        };
        return "Ping received and stored.";
    };

    /**
     * Publiczna funkcja, która pozwala właścicielowi (i każdemu innemu) sprawdzić ostatni otrzymany ping.
     * W docelowym rozwiązaniu funkcja ta powinna być zabezpieczona, aby tylko właściciel agenta mógł ją wywołać.
     * @return - Zwraca ostatni ping lub `null`, jeśli żaden nie został otrzymany.
     */
    public query func get_last_ping() : async ?Ping {
        return lastPing;
    };

}