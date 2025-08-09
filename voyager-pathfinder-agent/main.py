import asyncio
import ollama_handler
import voyager_connector
from pathlib import Path
import re

# --- Konfiguracja Narzędzi i Kanistrów ---
# UWAGA: Poniższe ID kanistrów są tymczasowe. Należy je zastąpić prawdziwymi ID po wdrożeniu.
MESSENGER_HUB_CANISTER_ID = "placeholder-messenger-hub-id"
# To powinien być ID osobistego kanistra tego konkretnego agenta
MY_PERSONAL_HUB_CANISTER_ID = "placeholder-personal-hub-id" 

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
    return await voyager_connector.call_canister(MY_PERSONAL_HUB_CANISTER_ID, "hello", [], DID_HELLOWORLD)

async def send_voyager_message(recipient_principal: str, message_content: str) -> str:
    """Wysyła asynchroniczną wiadomość do innego agenta VOYAGER przez publiczny messenger hub."""
    return await voyager_connector.call_canister(MESSENGER_HUB_CANISTER_ID, "send_message", [recipient_principal, message_content], DID_MESSENGER_HUB)

async def check_voyager_messages() -> str:
    """Sprawdza i odbiera nowe, asynchroniczne wiadomości ze swojej skrzynki w publicznym messenger hub."""
    return await voyager_connector.call_canister(MESSENGER_HUB_CANISTER_ID, "check_messages", [], DID_MESSENGER_HUB)

async def ping_voyager_agent(target_canister_id: str, message: str) -> str:
    """Wysyła bezpośredni 'ping' do osobistego kanistra innego agenta VOYAGER."""
    return await voyager_connector.call_canister(target_canister_id, "ping", [message], DID_PERSONAL_HUB)

async def check_my_pings() -> str:
    """Sprawdza swój osobisty kanister w poszukiwaniu ostatnich otrzymanych 'pingów'."""
    return await voyager_connector.call_canister(MY_PERSONAL_HUB_CANISTER_ID, "get_last_ping", [], DID_PERSONAL_HUB)

AVAILABLE_TOOLS = {
    "helloworld_tool": helloworld_tool,
    "send_voyager_message": send_voyager_message,
    "check_voyager_messages": check_voyager_messages,
    "ping_voyager_agent": ping_voyager_agent,
    "check_my_pings": check_my_pings,
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
