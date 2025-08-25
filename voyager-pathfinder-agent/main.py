import asyncio
import ollama_handler
from voyager_connector import VoyagerConnector, Conn, Voyager
from pathlib import Path
import re
from functools import partial

# --- Nowa, poprawiona sekcja inicjalizacji ---
# Bezpośrednia obsługa logiki z ic-py, aby poprawnie załadować tożsamość z pliku .pem
# i uniknąć modyfikacji kodu w agencie "panda".
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent

# --- Konfiguracja ---
# Jedyny wymagany na stałe ID to punkt wejścia do sieci - główny DataBox.
DATABOX_CANISTER_ID = "rrkah-fqaaa-aaaaa-aaaaq-cai" # Używam znanego publicznego ID jako przykładu

# Ścieżka do pliku tożsamości. Jeśli nie istnieje, zostanie utworzona nowa.
IDENTITY_PEM_PATH = Path(__file__).parent / "identity.pem"

def create_agent_with_identity(pem_path: Path) -> Agent:
    """Tworzy i zwraca agenta IC z tożsamością załadowaną z pliku PEM."""
    if pem_path.exists():
        print(f"Znaleziono istniejącą tożsamość w: {pem_path}")
        identity = Identity.from_pem(pem_path.read_bytes().decode('utf-8'))
    else:
        print(f"Nie znaleziono tożsamości, tworzę nową w: {pem_path}")
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

def create_dynamic_tool(canister_id: str, app_title: str, standard_name: str, function_name: str, *args_template):
    """Tworzy generyczną funkcję narzędzia dla danej aplikacji i standardu."""
    # Używamy partial, aby "zamrozić" argumenty, które znamy w momencie tworzenia narzędzia
    async def tool_func(*func_args):
        print(f"Wywołuję dynamiczne narzędzie: canister='{canister_id}', metoda='{function_name}', argumenty='{func_args}'")
        # Zakładamy, że voyager_conn ma metodę do wywoływania generycznych funkcji
        return await voyager_conn.call_app_method(canister_id, function_name, *func_args)
    
    # Tworzymy opis (docstring) dla modelu AI
    tool_func.__doc__ = f"Wywołuje funkcję '{function_name}' standardu '{standard_name}' w aplikacji '{app_title}' ({canister_id})."
    return tool_func

def register_tools_for_app(app_conn: Conn):
    """Rejestruje wszystkie narzędzia dla danej aplikacji na podstawie jej konektorów."""
    print(f"Rejestrowanie narzędzi dla aplikacji: '{app_conn.title}' ({app_conn.conn}) z konektorami: {app_conn.conector}")
    
    # Prosta mapa standardów na funkcje - można ją rozbudować
    # Klucz: nazwa standardu w `conector`. Wartość: lista tupli (nazwa funkcji, argumenty)
    standard_to_functions_map = {
        "help": [("help", (int,))],
        "hwoisme": [("hwoisme", ())],
        "glue": [("glue_get", (list,)), ("glue_push", (list,))],
        "ping": [("ping", (str,))]
        # Można dodać więcej standardów, np. 'file', 'conn', 'frend'
    }

    for standard in app_conn.conector:
        if standard in standard_to_functions_map:
            for func_name, args_template in standard_to_functions_map[standard]:
                # Tworzymy unikalną nazwę dla narzędzia
                tool_name = f"app_{app_conn.title.replace(' ', '_').lower()}_{func_name}"
                tool_function = create_dynamic_tool(app_conn.conn, app_conn.title, standard, func_name, args_template)
                AVAILABLE_TOOLS[tool_name] = tool_function
                print(f"  -> Zarejestrowano narzędzie: {tool_name}")

# --- Funkcje Pomocnicze ---
def parse_think_tags(content: str) -> str:
    """Usuwa tagi <think>...</think> z odpowiedzi modelu.""" 
    return re.sub(r'<think>.*?</think>\s*', '', content, flags=re.DOTALL).strip()

# --- Główna Logika Agenta ---
async def run_agent():
    """Główna pętla operacyjna agenta Pathfinder."""
    global AVAILABLE_TOOLS # Modyfikujemy globalną listę

    try:
        Path('persona.md').read_text(encoding='utf-8')
    except FileNotFoundError:
        print("OSTRZEŻENIE: Nie znaleziono pliku persona.md.")

    # Krok 1: Połącz z DataBoxem i odkryj dostępne aplikacje
    print(f"Łączenie z głównym DataBoxem: {DATABOX_CANISTER_ID}")
    try:
        voyager_conn.connect_to_databox(DATABOX_CANISTER_ID)
        print("Połączono z DataBoxem. Odkrywanie aplikacji (conn)...")
        
        i = 0
        while True:
            conn_entry = await voyager_conn.get_databox_conn_one(i)
            if conn_entry.conn == "NULL":
                break
            # Dla każdej odkrytej aplikacji, zarejestruj jej narzędzia
            register_tools_for_app(conn_entry)
            i += 1
        
        if not AVAILABLE_TOOLS:
            print("OSTRZEŻENIE: Nie odkryto żadnych aplikacji z obsługiwanymi standardami w DataBoxie.")

    except Exception as e:
        print(f"BŁĄD KRYTYCZNY podczas łączenia z DataBoxem lub odkrywania narzędzi: {e}")
        print("Agent nie może kontynuować pracy bez połączenia z DataBoxem. Zamykanie.")
        return

    # Krok 2: Uruchom pętlę konwersacji z dynamicznie załadowanymi narzędziami
    all_tools_list = list(AVAILABLE_TOOLS.values())
    conversation_history = [{'role': 'system', 'content': ollama_handler.SYSTEM_PROMPT}]
    
    print("\nPathfinder: Agent komunikacyjny VOYAGER gotowy. Wszystkie narzędzia załadowane dynamicznie.")
    print(f"Dostępne narzędzia: {list(AVAILABLE_TOOLS.keys())}")
    print("Wpisz 'wyjdź', aby zakończyć.")
    
    GREETINGS = ["siemka", "cześć", "witaj", "hej", "siema"]

    while True:
        user_prompt = input("Ty: ")
        if user_prompt.lower() == 'wyjdź':
            break

        if user_prompt.lower().strip() in GREETINGS:
            print("Pathfinder: Witaj na pokładzie. Jaką podróż dziś zaczynamy?")
            continue

        conversation_history.append({'role': 'user', 'content': user_prompt})
        response = ollama_handler.get_ai_response(conversation_history, all_tools_list)

        if not response:
            conversation_history.pop()
            continue

        response_message = response['message']
        conversation_history.append(response_message)

        if not response_message.get('tool_calls'):
            print(f"Pathfinder: {parse_think_tags(response_message['content'])}")
        else:
            tool_calls = response_message['tool_calls']
            for tool_call in tool_calls:
                tool_name = tool_call['function']['name']
                tool_args = tool_call['function']['arguments']
                confirm = input(f"Pathfinder: Model chce użyć narzędzia '{tool_name}' z argumentami {tool_args}. Zgadzasz się? [T/N]: ")

                if confirm.lower() == 't':
                    tool_function = AVAILABLE_TOOLS.get(tool_name)
                    if tool_function:
                        # Argumenty z modelu AI są w słowniku, trzeba je przekazać jako *args
                        # Zakładamy, że model poda argumenty w odpowiedniej kolejności
                        # Lepsze rozwiązanie to nazwane argumenty, ale to wymaga więcej logiki
                        args_list = list(tool_args.values())
                        result = await tool_function(*args_list)
                        print(f"Pathfinder: Odpowiedź z narzędzia: {result}")
                        conversation_history.append({'role': 'tool', 'content': str(result)}) # Upewnij się, że wynik jest stringiem
                        final_response = ollama_handler.get_ai_response(conversation_history, all_tools_list)
                        if final_response:
                            final_message = parse_think_tags(final_response['message']['content'])
                            print(f"Pathfinder: {final_message}")
                            conversation_history.append(final_response['message'])
                else:
                    print("Pathfinder: Odmówiono użycia narzędzia.")
                    # Usuwamy ostatnią wiadomość usera i próbę wywołania narzędzia przez AI
                    conversation_history.pop() 
                    conversation_history.pop()

if __name__ == "__main__":
    try:
        asyncio.run(run_agent())
    except KeyboardInterrupt:
        print("\nPathfinder: Przerwano eksplorację.")
