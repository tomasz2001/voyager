import asyncio
import ollama_handler
from voyager_connector import VoyagerConnector, Conn, Voyager
from pathlib import Path
import re, json
from functools import partial
from colorama import Fore, Style, init

# --- Nowa, poprawiona sekcja inicjalizacji ---
# Bezpośrednia obsługa logiki z ic-py, aby poprawnie załadować tożsamość z pliku .pem
# i uniknąć modyfikacji kodu w agencie "panda".
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent

# --- Konfiguracja ---
# Jedyny wymagany na stałe ID to punkt wejścia do sieci - główny DataBox.
DATABOX_CANISTER_ID = "wewn4-aqaaa-aaaam-qdxoa-cai" # Używam znanego publicznego ID jako przykładu

# Ścieżka do pliku tożsamości. Jeśli nie istnieje, zostanie utworzona nowa.
IDENTITY_PEM_PATH = Path(__file__).parent / "identity.pem"

def create_agent_with_identity(pem_path: Path) -> Agent:
    """Tworzy i zwraca agenta IC z tożsamością załadowaną z pliku PEM."""
    if pem_path.exists():
        print(f"{Fore.YELLOW}Znaleziono istniejącą tożsamość w: {pem_path}{Style.RESET_ALL}")
        identity = Identity.from_pem(pem_path.read_bytes().decode('utf-8'))
    else:
        print(f"{Fore.YELLOW}Nie znaleziono tożsamości, tworzę nową w: {pem_path}{Style.RESET_ALL}")
        identity = Identity()
        pem_path.parent.mkdir(parents=True, exist_ok=True)
        pem_path.write_bytes(identity.to_pem())

    client = Client(url="https://ic0.app")
    return Agent(identity, client)

# --- Inicjalizacja Konektorów ---
# Tworzymy agenta z poprawnie załadowaną tożsamością
ic_agent = create_agent_with_identity(IDENTITY_PEM_PATH)
# Przekazujemy agenta, a nie konektor z innego projektu
voyager_conn = VoyagerConnector(ic_agent) 

# --- Dynamiczne Tworzenie Narzędzi ---
AVAILABLE_TOOLS = {} # Zaczynamy z pustą mapą narzędzi

def create_dynamic_tool(tool_name: str, canister_id: str, app_title: str, standard_name: str, function_name: str, *args_template):
    """Tworzy generyczną funkcję narzędzia dla danej aplikacji i standardu."""
    # Używamy partial, aby "zamrozić" argumenty, które znamy w momencie tworzenia narzędzia
    async def tool_func(*func_args):
        print(f"{Fore.MAGENTA}Wywołuję dynamiczne narzędzie: canister='{canister_id}', metoda='{function_name}', argumenty='{func_args}'{Style.RESET_ALL}")
        # Zakładamy, że voyager_conn ma metodę do wywoływania generycznych funkcji
        return await voyager_conn.call_app_method(canister_id, function_name, *func_args)
    
    # KLUCZOWA POPRAWKA: Nadajemy funkcji unikalną nazwę, którą zobaczy model AI
    tool_func.__name__ = tool_name

    # Tworzymy opis (docstring) dla modelu AI
    tool_func.__doc__ = f"Wywołuje funkcję '{function_name}' standardu '{standard_name}' w aplikacji '{app_title}' ({canister_id})."
    return tool_func

def register_tools_for_app(app_conn: Conn):
    """Rejestruje wszystkie narzędzia dla danej aplikacji na podstawie jej konektorów."""
    print(f"{Fore.YELLOW}Rejestrowanie narzędzi dla aplikacji: '{app_conn.title}' ({app_conn.conn}) z konektorami: {app_conn.conector}{Style.RESET_ALL}")
    
    # Prosta mapa standardów na funkcje - można ją rozbudować
    # Klucz: nazwa standardu w `conector`. Wartość: lista tupli (nazwa funkcji, argumenty)
    standard_to_functions_map = {
        "help": [("help", (int,))],
        "hwoisme": [("hwoisme", ())],
        "glue": [("glue_get", (list,)), ("glue_push", (list,))],
        "ping": [("ping", (str,))]
    }

    for standard in app_conn.conector:
        # Specjalna obsługa dla problematycznego kanistra iruwa-4iaaa-aaaam-aemaq-cai
        if app_conn.conn == "iruwa-4iaaa-aaaam-aemaq-cai" and standard == "help":
            print(f"{Fore.YELLOW}  -> Pomijam rejestrację narzędzia 'help' dla {app_conn.title} ({app_conn.conn}) z powodu błędu kanistra.{Style.RESET_ALL}")
            continue

        if standard in standard_to_functions_map:
            for func_name, args_template in standard_to_functions_map[standard]:
                # Tworzymy unikalną nazwę dla narzędzia
                tool_name = f"app_{app_conn.title.replace(' ', '_').lower()}_{func_name}"
                # Przekazujemy unikalną nazwę do funkcji tworzącej
                tool_function = create_dynamic_tool(tool_name, app_conn.conn, app_conn.title, standard, func_name, args_template)
                AVAILABLE_TOOLS[tool_name] = tool_function
                print(f"{Fore.GREEN}  -> Zarejestrowano narzędzie: {tool_name}{Style.RESET_ALL}")

# --- Funkcje Pomocnicze ---
def parse_think_tags(content: str) -> str:
    """Usuwa tagi <think>...</think> z odpowiedzi modelu.""" 
    return re.sub(r'<think>.*?</think>\s*', '', content, flags=re.DOTALL).strip()

# --- Główna Logika Agenta ---
async def run_agent():
    """Główna pętla operacyjna agenta Pathfinder."""
    init(autoreset=True) # Inicjalizacja Colorama
    global AVAILABLE_TOOLS # Modyfikujemy globalną listę

    try:
        Path('persona.md').read_text(encoding='utf-8')
    except FileNotFoundError:
        print(f"{Fore.RED}OSTRZEŻENIE: Nie znaleziono pliku persona.md.{Style.RESET_ALL}")

    # Krok 1: Połącz z DataBoxem i odkryj dostępne aplikacje
    print(f"{Fore.YELLOW}Łączenie z głównym DataBoxem: {DATABOX_CANISTER_ID}{Style.RESET_ALL}")
    try:
        voyager_conn.connect_to_databox(DATABOX_CANISTER_ID)
        print(f"{Fore.GREEN}Połączono z DataBoxem. Odkrywanie aplikacji (conn)...{Style.RESET_ALL}")
        
        i = 0
        while True:
            conn_entry = await voyager_conn.get_databox_conn_one(i)
            if conn_entry.conn == "NULL":
                break
            # Dla każdej odkrytej aplikacji, zarejestruj jej narzędzia
            register_tools_for_app(conn_entry)
            i += 1
        
        if not AVAILABLE_TOOLS:
            print(f"{Fore.YELLOW}OSTRZEŻENIE: Nie odkryto żadnych aplikacji z obsługiwanymi standardami w DataBoxie.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}BŁĄD KRYTYCZNY podczas łączenia z DataBoxem lub odkrywania narzędzi: {e}{Style.RESET_ALL}")
        print(f"{Fore.RED}Agent nie może kontynuować pracy bez połączenia z DataBoxem. Zamykanie.{Style.RESET_ALL}")
        return

    # Krok 2: Uruchom pętlę konwersacji z dynamicznie załadowanymi narzędziami
    all_tools_list = list(AVAILABLE_TOOLS.values())
    conversation_history = [{'role': 'system', 'content': ollama_handler.SYSTEM_PROMPT}]
    
    print(f"\n{Fore.CYAN}Pathfinder:{Style.RESET_ALL} Agent komunikacyjny VOYAGER gotowy. Wszystkie narzędzia załadowane dynamicznie.")
    print(f"{Fore.CYAN}Dostępne narzędzia:{Style.RESET_ALL} {list(AVAILABLE_TOOLS.keys())}")
    print("Wpisz 'wyjdź', aby zakończyć.")
    
    GREETINGS = ["siemka", "cześć", "witaj", "hej", "siema"]

    while True:
        user_prompt = input(f"{Fore.GREEN}Ty: {Style.RESET_ALL}")
        cleaned_prompt = user_prompt.lower().strip()

        if cleaned_prompt == 'wyjdź':
            break

        if cleaned_prompt == '/clear':
            conversation_history = [{'role': 'system', 'content': ollama_handler.SYSTEM_PROMPT}]
            print(f"\n{Fore.YELLOW}--- Kontekst rozmowy wyczyszczony ---{Style.RESET_ALL}\n")
            continue
        
        if cleaned_prompt == '/tools':
            print(f"\n{Fore.CYAN}--- Dostępne narzędzia ---{Style.RESET_ALL}")
            if AVAILABLE_TOOLS:
                for tool_name in AVAILABLE_TOOLS.keys():
                    print(f"- {tool_name}")
            else:
                print(f"{Fore.YELLOW}Brak dynamicznie załadowanych narzędzi.{Style.RESET_ALL}")
            print(f"{Fore.CYAN}-------------------------{Style.RESET_ALL}\n")
            continue

        if cleaned_prompt == '/help':
            print(f"""\n{Fore.CYAN}--- Pomoc Agenta Pathfinder ---
{Style.RESET_ALL}Jestem inteligentnym przewodnikiem po zdecentralizowanej sieci VOYAGER.
Możesz ze mną rozmawiać w języku naturalnym lub używać poniższych komend:

{Style.BRIGHT}Komendy:{Style.RESET_ALL}
  /help      - Wyświetla tę wiadomość pomocy.
  /clear     - Resetuje historię konwersacji.
  /tools     - Wyświetla listę dynamicznie załadowanych narzędzi.
  wyjdź      - Kończy pracę z agentem.
{Fore.CYAN}-----------------------------------{Style.RESET_ALL}\n""")
            continue

        if cleaned_prompt in GREETINGS:
            print(f"{Fore.CYAN}Pathfinder:{Style.RESET_ALL} Witaj na pokładzie. Jaką podróż dziś zaczynamy?")
            continue

        conversation_history.append({'role': 'user', 'content': user_prompt})
        response = ollama_handler.get_ai_response(conversation_history, all_tools_list)

        if not response:
            conversation_history.pop()
            continue

        response_message = response['message']
        conversation_history.append(response_message)

        if not response_message.get('tool_calls'):
            # Sprawdzamy, czy model nie "wypisał" tool-calla bezpośrednio w treści
            tool_call_match = re.search(r'<tool>(.*?)</tool>', response_message['content'], re.DOTALL)
            if tool_call_match:
                tool_call_json = ""
                try:
                    tool_call_json = tool_call_match.group(1)
                    parsed_tool_call = json.loads(tool_call_json)
                    # Tworzymy sztuczną strukturę tool_calls
                    tool_calls = [{'function': parsed_tool_call}]
                    # Usuwamy tool-call z treści, aby nie był wyświetlany użytkownikowi
                    response_message['content'] = re.sub(r'<tool>.*?</tool>', '', response_message['content'], flags=re.DOTALL).strip()
                except json.JSONDecodeError:
                    print(f"{Fore.RED}BŁĄD: Nie udało się sparsować tool-calla z treści: {tool_call_json}{Style.RESET_ALL}")
                    tool_calls = [] # Traktujemy jako brak tool-calla
            else:
                tool_calls = [] # Brak tool-calla w treści
        else:
            tool_calls = response_message['tool_calls']

        if not tool_calls:
            print(f"{Fore.CYAN}Pathfinder: {Style.RESET_ALL}{parse_think_tags(response_message['content'])}")
        else:
            # Reszta logiki obsługi tool-calli pozostaje bez zmian
            for tool_call in tool_calls:
                tool_name = tool_call['function']['name']
                tool_args = tool_call['function']['arguments']
                confirm = input(f"{Fore.YELLOW}Pathfinder: Model chce użyć narzędzia '{tool_name}' z argumentami {tool_args}. Zgadzasz się? [T/N]: {Style.RESET_ALL}")

                if confirm.lower() == 't':
                    tool_function = AVAILABLE_TOOLS.get(tool_name)
                    if tool_function:
                        # Argumenty z modelu AI są w słowniku, trzeba je przekazać jako *args
                        # Zakładamy, że model poda argumenty w odpowiedniej kolejności
                        # Lepsze rozwiązanie to nazwane argumenty, ale to wymaga więcej logiki
                        args_list = list(tool_args.values())
                        result = await tool_function(*args_list)
                        print(f"{Fore.MAGENTA}Pathfinder: Odpowiedź z narzędzia: {result}{Style.RESET_ALL}")
                        conversation_history.append({'role': 'tool', 'content': str(result)}) # Upewnij się, że wynik jest stringiem
                        final_response = ollama_handler.get_ai_response(conversation_history, all_tools_list)
                        if final_response:
                            final_message = parse_think_tags(final_response['message']['content'])
                            print(f"{Fore.CYAN}Pathfinder: {Style.RESET_ALL}{final_message}")
                            conversation_history.append(final_response['message'])
                else:
                    print(f"{Fore.YELLOW}Pathfinder: Odmówiono użycia narzędzia.{Style.RESET_ALL}")
                    # Usuwamy ostatnią wiadomość usera i próbę wywołania narzędzia przez AI
                    conversation_history.pop() 
                    conversation_history.pop()

if __name__ == "__main__":
    try:
        asyncio.run(run_agent())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Pathfinder: Przerwano eksplorację.{Style.RESET_ALL}")
