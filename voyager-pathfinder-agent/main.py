import asyncio
import ollama_handler
from voyager_connector import VoyagerConnector, Conn, Voyager # Import the updated VoyagerConnector and data classes
from voyager_py_agent_panda.ic_connector import ICConnector # Import ICConnector
from pathlib import Path
import re

# --- Konfiguracja Narzędzi i Kanistrów ---
# UWAGA: Poniższe ID kanistrów są tymczasowe. Należy je zastąpić prawdziwymi ID po wdrożeniu.
MESSENGER_HUB_CANISTER_ID = "placeholder-messenger-hub-id"
MY_PERSONAL_HUB_CANISTER_ID = "placeholder-personal-hub-id"

# Placeholder for DataBox Canister ID
DATABOX_CANISTER_ID = "placeholder-databox-id" # <<<--- IMPORTANT: Replace with actual DataBox Canister ID

# Path to your identity.pem file for IC authentication
IDENTITY_PEM_PATH = Path(__file__).parent.parent / "voyager-py-agent-panda" / "identity.pem" # Adjust path as needed

# --- Initialize ICConnector and VoyagerConnector ---
ic_connector = ICConnector(IDENTITY_PEM_PATH)
voyager_conn = VoyagerConnector(ic_connector)

# Definicje interfejsów DID dla kanistrów
DID_HELLOWORLD = "service: { \"hello\": () -> (text) query; }"
DID_MESSENGER_HUB = """
service: {
  "send_message": (principal, text) -> ();
  "check_messages": () -> (vec text);
}
"""
DID_PERSONAL_HUB = """
service: {
  "ping": (text) -> (text);
  "get_last_ping": () -> (opt record { from: principal; message: text; timestamp: nat64 });
}
"""

# --- Definicje Dostępnych Narzędzi ---

async def helloworld_tool() -> str:
    """Wywołuje proste narzędzie 'helloworld' w sieci VOYAGER, aby sprawdzić, czy komunikacja działa."""
    # This will now use the voyager_conn to call the app method
    return await voyager_conn.call_app_method(MY_PERSONAL_HUB_CANISTER_ID, "hello")

async def send_voyager_message(recipient_principal: str, message_content: str) -> str:
    """Wysyła asynchroniczną wiadomość do innego agenta VOYAGER przez publiczny messenger hub."""
    return await voyager_conn.call_app_method(MESSENGER_HUB_CANISTER_ID, "send_message", recipient_principal, message_content)

async def check_voyager_messages() -> str:
    """Sprawdza i odbiera nowe, asynchroniczne wiadomości ze swojej skrzynki w publicznym messenger hub."""
    return await voyager_conn.call_app_method(MESSENGER_HUB_CANISTER_ID, "check_messages")

async def ping_voyager_agent(target_canister_id: str, message: str) -> str:
    """Wysyła bezpośredni 'ping' do osobistego kanistra innego agenta VOYAGER."""
    return await voyager_conn.call_app_method(target_canister_id, "ping", message)

async def check_my_pings() -> str:
    """Sprawdza swój osobisty kanister w poszukiwaniu ostatnich otrzymanych 'pingów'."""
    return await voyager_conn.call_app_method(MY_PERSONAL_HUB_CANISTER_ID, "get_last_ping")

# New tools for DataBox interaction
async def get_databox_help_tool(line: int = 0) -> str:
    """Pobiera pomoc z podłączonego DataBoxa."""
    return await voyager_conn.get_databox_help(line)

async def get_databox_hwoisme_tool() -> Conn:
    """Pobiera meta informacje o podłączonym DataBoxie."""
    return await voyager_conn.get_databox_hwoisme()

async def get_databox_frend_one_tool(index: int) -> Voyager:
    """Pobiera informacje o innym DataBoxie z listy frend."""
    return await voyager_conn.get_databox_frend_one(index)

async def get_databox_conn_one_tool(index: int) -> Conn:
    """Pobiera informacje o aplikacji z listy conn."""
    return await voyager_conn.get_databox_conn_one(index)

AVAILABLE_TOOLS = {
    "helloworld_tool": helloworld_tool,
    "send_voyager_message": send_voyager_message,
    "check_voyager_messages": check_voyager_messages,
    "ping_voyager_agent": ping_voyager_agent,
    "check_my_pings": check_my_pings,
    "get_databox_help_tool": get_databox_help_tool,
    "get_databox_hwoisme_tool": get_databox_hwoisme_tool,
    "get_databox_frend_one_tool": get_databox_frend_one_tool,
    "get_databox_conn_one_tool": get_databox_conn_one_tool,
}
ALL_TOOLS_LIST = list(AVAILABLE_TOOLS.values())

# --- Funkcje Pomocnicze ---
def parse_think_tags(content: str) -> str:
    """Usuwa tagi <think>...</think> z odpowiedzi modelu.""" 
    return re.sub(r'<think>.*?</think>\s*', '', content, flags=re.DOTALL).strip()

# --- Główna Logika Agenta ---
async def run_agent():
    """Główna pętla operacyjna agenta Pathfinder."""
    try:
        Path('persona.md').read_text(encoding='utf-8')
    except FileNotFoundError:
        print("OSTRZEŻENIE: Nie znaleziono pliku persona.md.")

    # Connect to the DataBox
    print(f"Attempting to connect to DataBox with ID: {DATABOX_CANISTER_ID}")
    try:
        voyager_conn.connect_to_databox(DATABOX_CANISTER_ID)
        print("Successfully connected to DataBox.")
        # Example DataBox interaction
        databox_meta = await voyager_conn.get_databox_hwoisme()
        print(f"DataBox Meta: {databox_meta}")
        databox_help = await voyager_conn.get_databox_help(0)
        print(f"DataBox Help (0): {databox_help}")

        # Discover frend and conn (applications)
        print("\nDiscovering other DataBoxes (frend):")
        i = 0
        while True:
            frend_entry = await voyager_conn.get_databox_frend_one(i)
            if frend_entry.conn == "NULL":
                break
            print(f"  Frend {i}: {frend_entry}")
            i += 1

        print("\nDiscovering applications (conn):")
        i = 0
        while True:
            conn_entry = await voyager_conn.get_databox_conn_one(i)
            if conn_entry.conn == "NULL":
                break
            print(f"  App {i}: {conn_entry}")
            # Here you could dynamically add tools to interact with this app
            # based on its conector list. This is a more advanced step.
            i += 1

    except Exception as e:
        print(f"Błąd podczas łączenia z DataBoxem lub interakcji: {e}")
        print("Kontynuowanie działania agenta bez połączenia z DataBoxem.")


    conversation_history = [{
        'role': 'system',
        'content': ollama_handler.SYSTEM_PROMPT
    }]
    print("\nPathfinder: Agent komunikacyjny VOYAGER gotowy. Wpisz 'wyjdź', aby zakończyć.")
    GREETINGS = ["siemka", "cześć", "witaj", "hej", "siema"]

    while True:
        user_prompt = input("Ty: ")
        if user_prompt.lower() == 'wyjdź':
            break

        if user_prompt.lower().strip() in GREETINGS:
            print("Pathfinder: Witaj na pokładzie. Jaką podróż dziś zaczynamy?")
            continue

        conversation_history.append({'role': 'user', 'content': user_prompt})
        response = ollama_handler.get_ai_response(conversation_history, ALL_TOOLS_LIST)

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
                        result = await tool_function(**tool_args)
                        print(f"Pathfinder: Odpowiedź z narzędzia: {result}")
                        conversation_history.append({'role': 'tool', 'content': result})
                        final_response = ollama_handler.get_ai_response(conversation_history, ALL_TOOLS_LIST)
                        if final_response:
                            final_message = parse_think_tags(final_response['message']['content'])
                            print(f"Pathfinder: {final_message}")
                            conversation_history.append(final_response['message'])
                else:
                    print("Pathfinder: Odmówiono użycia narzędzia.")
                    conversation_history.pop()
                    conversation_history.pop()

if __name__ == "__main__":
    try:
        asyncio.run(run_agent())
    except KeyboardInterrupt:
        print("\nPathfinder: Przerwano eksplorację.")