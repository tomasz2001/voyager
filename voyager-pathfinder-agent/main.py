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

# Import ICConnector from the new tools directory
from tools.ic_connector import ICConnector

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
AVAILABLE_TOOLS: dict = {} # Zaczynamy z pustą mapą narzędzi
DISCOVERED_APPS = [] # Lista do przechowywania odkrytych aplikacji

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
        "ping": [("ping", (str,))],
        "set_canister_id": [("set_canister_id", (str,))],
        "get_app": [("get_app", (int,))],
        "get_box": [("get_box", (int,))],
        "use_glue_get": [("use_glue_get", (list,))],
        "use_glue_push": [("use_glue_push", (list,))],
        "get_help": [("get_help", (int,))],
    }

    for standard in app_conn.conector:

        if standard in standard_to_functions_map:
            for func_name, args_template in standard_to_functions_map[standard]:
                # Tworzymy unikalną nazwę dla narzędzia
                tool_name = f"app_{app_conn.title.replace(' ', '_').lower()}_{func_name}"
                # Przekazujemy unikalną nazwę do funkcji tworzącej
                tool_function = create_dynamic_tool(tool_name, app_conn.conn, app_conn.title, standard, func_name, args_template)
                AVAILABLE_TOOLS[tool_name] = tool_function
                print(f"{Fore.GREEN}  -> Zarejestrowano narzędzie: {tool_name}{Style.RESET_ALL}")

def create_panda_tool_wrapper(original_func, tool_name, description, parameters, required):
    async def wrapper(**kwargs):
        # Filter kwargs to only include those expected by the original_func
        # This assumes 'parameters' correctly reflects the expected arguments of original_func
        final_kwargs = {k: v for k, v in kwargs.items() if k in parameters}
        
        # Ensure all required parameters are present
        for req_param in required:
            if req_param not in final_kwargs:
                # This case should ideally be caught by the model's tool calling logic,
                # but it's good to have a safeguard.
                raise ValueError(f"Missing required parameter: {req_param} for tool {tool_name}")

        return await original_func(**final_kwargs)

    wrapper.__name__ = tool_name
    wrapper.__doc__ = description
    setattr(wrapper, '__tool_schema__', {
        'type': 'function',
        'function': {
            'name': tool_name,
            'description': description,
            'parameters': {
                'type': 'object',
                'properties': parameters,
                'required': required,
            },
        },
    })
    return wrapper

def register_panda_tools(ic_connector_instance: ICConnector):
    """Registers tools from ICConnector to the AVAILABLE_TOOLS."""
    global AVAILABLE_TOOLS

    tools_to_register = [
        {
            'name': 'set_canister_id',
            'func': ic_connector_instance.set_canister_id,
            'description': 'Sets the target canister ID for all subsequent communication.',
            'parameters': {'canister_id': {'type': 'string', 'description': 'The new canister ID to target.'}},
            'required': ['canister_id'],
        },
        {
            'name': 'hwoisme',
            'func': ic_connector_instance.hwoisme,
            'description': 'Checks who the agent is talking to and what interfaces the canister has.',
            'parameters': {},
            'required': [],
        },
        {
            'name': 'get_app',
            'func': ic_connector_instance.get_app,
            'description': 'Fetches information about a specific application (conn) by its index from the current databox.',
            'parameters': {'index': {'type': 'integer', 'description': 'The index of the application to fetch.'}},
            'required': ['index'],
        },
        {
            'name': 'get_box',
            'func': ic_connector_instance.get_box,
            'description': 'Fetches information about a specific databox (frend) by its index from the current databox.',
            'parameters': {'index': {'type': 'integer', 'description': 'The index of the databox to fetch.'}},
            'required': ['index'],
        },
        {
            'name': 'use_glue_get',
            'func': ic_connector_instance.use_glue_get,
            'description': "Uses the 'glue_get' interface with the selected target. Typically used to read data, like posts.",
            'parameters': {'data': {'type': 'array', 'items': {'type': 'string'}, 'description': "A list of strings, where the first is the command (e.g., 'watch') and subsequent are arguments (e.g., post number)."}},
            'required': ['data'],
        },
        {
            'name': 'use_glue_push',
            'func': ic_connector_instance.use_glue_push,
            'description': "Uses the 'glue_push' interface to send data to the target. Typically used to create new content, like posts.",
            'parameters': {'data': {'type': 'array', 'items': {'type': 'string'}, 'description': "A list of strings, where the first is the command (e.g., 'post') and subsequent are arguments (e.g., nick, content)."}},
            'required': ['data'],
        },
        {
            'name': 'get_help',
            'func': ic_connector_instance.get_help,
            'description': 'Gets a specific help page from the service canister.',
            'parameters': {'page': {'type': 'integer', 'description': 'The page number of the help text to retrieve.'}},
            'required': ['page'],
        },
        {
            'name': 'get_help_all',
            'func': ic_connector_instance.get_help_all,
            'description': 'Retrieves all available help pages from the service canister until an error is encountered.',
            'parameters': {},
            'required': [],
        },
    ]

    for tool_spec in tools_to_register:
        tool_name = tool_spec['name']
        original_func = tool_spec['func']
        description = tool_spec['description']
        parameters = tool_spec['parameters']
        required = tool_spec['required']

        wrapped_tool_func = create_panda_tool_wrapper(
            original_func, tool_name, description, parameters, required
        )
        AVAILABLE_TOOLS[tool_name] = wrapped_tool_func
        print(f"{Fore.GREEN}  -> Zarejestrowano narzędzie Panda: {tool_name}{Style.RESET_ALL}")


# --- Funkcje Pomocnicze ---
def parse_think_tags(content: str) -> str:
    """Usuwa tagi <think>...</think> z odpowiedzi modelu."""
    return re.sub(r'<think>.*?</think>\s*', '', content, flags=re.DOTALL).strip()

# --- Główna Logika Agenta ---
async def run_agent():
    """Główna pętla operacyjna agenta Pathfinder."""
    global AVAILABLE_TOOLS # Modyfikujemy globalną listę
    init(autoreset=True) # Inicjalizacja Colorama

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
            DISCOVERED_APPS.append(conn_entry)
            i += 1
        
        if not AVAILABLE_TOOLS:
            print(f"{Fore.YELLOW}OSTRZEŻENIE: Nie odkryto żadnych aplikacji z obsługiwanymi standardami w DataBoxie.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}BŁĄD KRYTYCZNY podczas łączenia z DataBoxem lub odkrywania narzędzi: {e}{Style.RESET_ALL}")
        print(f"{Fore.RED}Agent nie może kontynuować pracy bez połączenia z DataBoxem. Zamykanie.{Style.RESET_ALL}")
        return

    # Instantiate ICConnector and register its tools
    ic_connector_instance = ICConnector(agent=ic_agent)
    register_panda_tools(ic_connector_instance)

    # Krok 2: Uruchom pętlę konwersacji z dynamicznie załadowanymi narzędziami
    # Explicitly ensure Pylance knows this is a dict
    if not isinstance(AVAILABLE_TOOLS, dict):
        AVAILABLE_TOOLS = {} # Re-initialize if somehow it's not a dict (shouldn't happen)

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
            print(f"{Fore.CYAN}-------------------------")
            continue

        elif cleaned_prompt.startswith('/list'):
            list_parts = cleaned_prompt.split(' ', 2) # Split into max 3 parts: '/list', 'set', '<index>'
            
            if len(list_parts) == 3 and list_parts[1] == 'set':
                try:
                    idx = int(list_parts[2])
                    if 0 <= idx < len(DISCOVERED_APPS):
                        selected_app = DISCOVERED_APPS[idx]
                        print(f"{Fore.CYAN}Pathfinder: Ustawiam komunikację na kanister: {selected_app.title} ({selected_app.conn}){Style.RESET_ALL}")
                        
                        # Set the canister ID
                        result = await ic_connector_instance.set_canister_id(canister_id=selected_app.conn)
                        print(f"{Fore.MAGENTA}Pathfinder: {result}{Style.RESET_ALL}")

                        # Re-register tools based on the selected app's connectors
                        # Clear existing dynamic tools
                        AVAILABLE_TOOLS = {}
                        
                        # Register tools for the selected app
                        register_tools_for_app(selected_app)
                        
                        # Re-register panda tools (general tools)
                        register_panda_tools(ic_connector_instance)

                        print(f"{Fore.CYAN}Pathfinder: Dostępne narzędzia zostały zaktualizowane dla kanistra {selected_app.title}.{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}Nowe dostępne narzędzia:{Style.RESET_ALL} {list(AVAILABLE_TOOLS.keys())}")

                    else:
                        print(f"{Fore.RED}Pathfinder: Nieprawidłowy indeks aplikacji. Użyj /list, aby zobaczyć dostępne indeksy.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Pathfinder: Nieprawidłowy format indeksu. Użyj /list set <numer_indeksu>.{Style.RESET_ALL}")
            elif len(list_parts) == 1: # Just '/list'
                print(f"\n{Fore.CYAN}--- Dostępne Aplikacje Voyager (Databox) ---{Style.RESET_ALL}")
                if DISCOVERED_APPS:
                    for idx, app in enumerate(DISCOVERED_APPS):
                        print(f"- {idx}. Tytuł: {app.title}, ID: {app.conn}, Konektory: {', '.join(app.conector)}")
                else:
                    print(f"{Fore.YELLOW}Brak odkrytych aplikacji w DataBoxie.{Style.RESET_ALL}")
                print(f"{Fore.CYAN}-------------------------------------------{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Pathfinder: Nieznana komenda /list. Użyj /list lub /list set <numer_indeksu>.{Style.RESET_ALL}")
            continue

        if cleaned_prompt == '/help':
            print(
                f"""{Fore.CYAN}--- Pomoc Agenta Pathfinder ---
Możesz ze mną rozmawiać w języku naturalnym lub używać poniższych komend:

{Style.BRIGHT}Komendy:{Style.RESET_ALL}
  /help        - Wyświetla tę wiadomość pomocy.
  /clear       - Resetuje historię konwersacji.
  /tools       - Wyświetla listę dynamicznie załadowanych narzędzi.
  /list        - Wyświetla wszystkie odkryte aplikacje Voyager w DataBoxie.
  /setcontainer - Ręcznie ustawia ID kanistra do komunikacji.
  wyjdź        - Kończy pracę z agentem.
{Fore.CYAN}-----------------------------------""")
            continue

        elif cleaned_prompt.startswith('/setcanister'):
            parts = cleaned_prompt.split(' ', 1)
            canister_id_input = None
            if len(parts) > 1:
                canister_id_input = parts[1].strip()

            if not canister_id_input:
                canister_id_input = input(f"{Fore.YELLOW}Podaj ID kanistra do ustawienia: {Style.RESET_ALL}")

            if canister_id_input:
                print(f"{Fore.CYAN}Pathfinder: Ustawiam ID kanistra na: {canister_id_input}{Style.RESET_ALL}")
                try:
                    result = await ic_connector_instance.set_canister_id(canister_id=canister_id_input)
                    print(f"{Fore.MAGENTA}Pathfinder: {result}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Pathfinder: Błąd podczas ustawiania ID kanistra: {e}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Pathfinder: Anulowano ustawianie ID kanistra. Nie podano ID.{Style.RESET_ALL}")
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
                if isinstance(tool_args, dict) and len(tool_args) == 1 and 'kwargs' in tool_args and isinstance(tool_args['kwargs'], str):
                    malformed_str = tool_args['kwargs']
                    try:
                        # Attempt to parse the malformed string "key: value" into a dictionary
                        # This is a fragile parsing, assuming a simple "key: value" format
                        parts = malformed_str.split(':', 1)
                        if len(parts) == 2:
                            key = parts[0].strip()
                            value = parts[1].strip()
                            tool_args = {key: value}
                            print(f"{Fore.YELLOW}WARNING: Corrected malformed tool arguments from string: {malformed_str} to {tool_args}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}ERROR: Could not parse malformed tool argument string: {malformed_str}{Style.RESET_ALL}")
                            # If parsing fails, keep original tool_args, it will likely lead to error
                    except Exception as e:
                        print(f"{Fore.RED}ERROR: Exception during malformed tool argument parsing: {e}{Style.RESET_ALL}")
                        # If any exception during parsing, keep original tool_args

                confirm = input(f"{Fore.YELLOW}Pathfinder: Model chce użyć narzędzia '{tool_name}' z argumentami {tool_args}. Zgadzasz się? [T/N]: {Style.RESET_ALL}")

                if confirm.lower() == 't':
                    tool_function = AVAILABLE_TOOLS.get(tool_name)
                    if tool_function:
                        # Przekazujemy argumenty jako kwargs dla lepszej niezawodności
                        result = await tool_function(**tool_args)
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
