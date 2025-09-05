import Principal "mo:base/Principal";
import HashMap "mo:base/HashMap";
import Buffer "mo:base/Buffer";

/**
 * Kanister VOYAGER Messenger Hub
 * Działa jak zdecentralizowana, asynchroniczna skrzynka pocztowa dla agentów VOYAGER.
 * Wiadomości są przechowywane do momentu ich odebrania przez adresata.
 */
actor {

    // Używamy stabilnej pamięci, aby wiadomości przetrwały aktualizacje kanistra.
    // Kluczem jest Principal ID agenta-odbiorcy.
    // Wartością jest bufor (dynamiczna tablica) z wiadomościami tekstowymi.
    stable var mailboxes = HashMap.HashMap<Principal, Buffer.Buffer<Text>>(0, Principal.equal, Principal.hash);

    /**
     * Wysyła wiadomość do określonego odbiorcy (identyfikowanego przez Principal).
     * @param to - Principal ID odbiorcy.
     * @param message - Treść wiadomości.
     */
    public shared (msg) func send_message(to: Principal, message: Text) : async () {
        // Pobieramy skrzynkę odbiorcy. Jeśli nie istnieje, tworzymy nową.
        let mailbox = switch (mailboxes.get(to)) {
            case (null) { Buffer.Buffer<Text>(1); };
            case (?buf) { buf };
        };
        // Dodajemy nową wiadomość do skrzynki.
        mailbox.add(message);
        // Aktualizujemy mapę z nową/zmienioną skrzynką.
        mailboxes.put(to, mailbox);
    };

    /**
     * Sprawdza i odbiera wszystkie wiadomości oczekujące na agenta, który wywołuje tę funkcję.
     * Po odebraniu, skrzynka jest czyszczona.
     * @return - Zwraca tablicę z wiadomościami. Jeśli brak, tablica jest pusta.
     */
    public shared (msg) func check_messages() : async [Text] {
        let caller = msg.caller;
        let mailbox = mailboxes.get(caller);

        switch (mailbox) {
            case (null) {
                // Jeśli skrzynka nie istnieje, zwracamy pustą tablicę.
                return [];
            };
            case (?buf) {
                // Jeśli wiadomości istnieją, usuwamy skrzynkę (aby ją opróżnić)
                // i zwracamy jej zawartość.
                mailboxes.delete(caller);
                return Buffer.toArray(buf);
            };
        };
    };
}