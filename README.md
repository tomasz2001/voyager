PROJEKT PUBLIC CHAT
TELEGRAM = [https://t.me/voyager_system]

LICENCE = "AGPLv3"
NAME = "VOYAGER"



🧭 Plan działania systemu Voyager

🔹 Czym jest Voyager?
Voyager to otwarta struktura do katalogowania usług i informacji, zbudowana na bazie zdecentralizowanej sieci (ICP). To nie jedna aplikacja — to zestaw komponentów, z których każdy może stworzyć własnego „agenta” do komunikacji z danymi lub usługami.

Voyager nie narzuca ci jednej aplikacji. Ty decydujesz, jakie interfejsy chcesz obsługiwać, i jakie dane chcesz udostępniać.

🔹 Jak działa?
System składa się z dwóch głównych elementów:

Voyager-DataBox (canister) – trzyma dane o usługach Voyager-App, innych Voyagerach-DataBox, oraz ich interfejsach (np. API, komendy, dostępność).

Aplikacje Voyager – łączą się z danymi i udostępniają interfejsy (np. ASCII-chat jako glue interface).

Te komponenty komunikują się przez prosty i otwarty system "standardów", który każdy może współtworzyć.

🧠 AI? Kiedy i jak?
Obecnie Voyager nie zawiera wbudowanego agenta AI, ale:

architektura zakłada możliwość dodania lokalnego AI, który korzysta z metadanych (conector[], title, conn) bez potrzeby interfejsów graficznych;

dane są już uporządkowane i czytelne dla modeli językowych, więc łatwo z tego zbudować narzędzie AI-ready;

np. przyszły agent może przeszukiwać sieć Voyagerów po słowach kluczowych w title i conector.

🔓 Otwarte, ludzkie standardy
W Voyagerze standardy komunikacyjne nie są pisane przez korporacje czy fundacje, ale przez użytkowników. Jak?

Każdy Conn zawiera pole conector[], które definiuje, jakie interfejsy są obsługiwane.

Przykład: ["glue", "help"] oznacza, że aplikacja wspiera standard glue, który pozwala np. dodawać posty.

Brak centralnego walidatora – jeśli chcesz stworzyć nowy standard ascii-market:0.1, po prostu go zdefiniuj i opublikuj.

To oznacza, że:

Możesz tworzyć usługi, które „gadają” między sobą — bez API gatewaya, bez Google, bez App Store.

🕸 Sieć zdecentralizowana naprawdę
Każdy Voyager-DataBox jest niezależnym węzłem, który:

przechowuje dane o innych Voyagerach (frend buffer),

trzyma wpisy o usługach (Conn buffer),

nie podlega kontroli żadnej firmy – kod działa na ICP, ale właścicielem danych jest użytkownik (Principal).

Nie musisz pytać Google ani Amazon o pozwolenie, by tworzyć własną infrastrukturę.

🎯 Nasz cel
Stworzyć żywy system wymiany informacji, w którym:

użytkownik sam tworzy katalog usług,

AI może z tym rozmawiać bez "frontendu",

a dane są zdecentralizowane, otwarte i odporne na cenzurę.

Nie chodzi o to, żebyś tworzył kolejną przeglądarkę.
Chodzi o to, żebyś stworzył swój własny internet.




Ktoś rzucił, że to "to samo co Ceneo"...
Szczerze? Męczy mnie już tłumaczenie coraz bardziej technicznych różnic. LEEEEEL

| **Cecha**                  | **CENEO**                                                                    | **VOYAGER (DVX)**                                                                                                                          |
| -------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Typ bazy**               | Scentralizowana – jedna baza danych zarządzana centralnie                    | Rozproszona – każdy węzeł (DataBox) to niezależna instancja, która może udostępniać i przechowywać dane o usługach lub innych Voyagerach   |
| **Własność danych**        | W całości należy do jednej firmy (Ceneo)                                     | Każdy użytkownik może hostować dane: swoje **i cudze**                                                                                     |
| **Dostępność**             | Tylko przez infrastrukturę firmy, narażona na awarie i zamknięcie            | Zawsze online – dane rozproszone między wielu niezależnych hostów, trudne do wyłączenia lub ocenzurowania                                  |
| **Dodawanie danych**       | Poprzez API kontrolowane przez centralny podmiot                             | Każdy może wystawić dane/usługi bez pytania o zgodę – wystarczy własny Voyager-DataBox lub dodanie wpisu do istniejącego                   |
| **Integracja z AI**        | Brak lub tylko marketingowe hasła                                            | System tworzony z myślą o integracji z agentami AI którzy mogą automatycznie wyszukiwać i porównywać usługi [[ gants-is-coming ]]          |
| **Trwałość projektu**      | Jeśli firma padnie – system znika                                            | Projekt przetrwa nawet jeśli twórcy znikną – każdy Voyager działa niezależnie i może być utrzymywany przez społeczność lub jednostki       |
| **Kontrola**               | Właściciel może blokować, modyfikować lub cenzurować dane                    | Nie ma pojedynczego punktu kontroli – dane są trwale rozproszone, a dostęp do nich jest otwarty i trudny do scentralizowanego ograniczenia |
| **Zdolność do współpracy** | Ograniczona do tego, co firma udostępni (np. brak dostępu do pełnych danych) | Voyagery mogą znać się nawzajem – DataBox może przechowywać adresy innych Voyagerów, tworząc sieć wzajemnych odniesień i źródeł danych     |


