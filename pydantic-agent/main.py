import asyncio
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
from config import Settings
from llm_clients import get_llm_client
from tools import ALL_TOOLS, get_tool_schema

async def main():
    # 1. Załadowanie konfiguracji
    load_dotenv()
    settings = Settings()
    print(f"Agent Mode: {settings.agent_mode}")
    print(f"MCP Server URL: {settings.mcp_server_url}")

    # 2. Inicjalizacja klienta LLM
    llm_client = get_llm_client(settings)

    # Przygotowanie narzędzi dla LLM
    if settings.agent_mode == 'openai':
        # Dla OpenAI, potrzebujemy schematów JSON
        llm_tools = [get_tool_schema(tool['function'], tool['input_model']) for tool in ALL_TOOLS]
    else:
        # Dla Ollamy, przekazujemy bezpośrednio funkcje
        llm_tools = [tool['function'] for tool in ALL_TOOLS]

    print("Agent gotowy. Wpisz 'exit' aby zakończyć.")

    # 3. Główna pętla interakcji
    while True:
        user_input = input("\nTy: ")
        if user_input.lower() == 'exit':
            break

        messages: List[Dict[str, Any]] = [{'role': 'user', 'content': user_input}]

        try:
            # Wywołanie LLM z narzędziami
            response = await llm_client(user_input, settings, llm_tools)

            # Sprawdzenie, czy LLM chce wywołać narzędzie
            tool_calls = []
            if settings.agent_mode == 'openai':
                # OpenAI API zwraca tool_calls w response.choices[0].message.tool_calls
                if response and response.get('choices') and response['choices'][0].get('message') and response['choices'][0]['message'].get('tool_calls'):
                    tool_calls = response['choices'][0]['message']['tool_calls']
            elif settings.agent_mode == 'ollama':
                # Ollama zwraca tool_calls w response.message.tool_calls
                if response and response.get('message') and response['message'].get('tool_calls'):
                    tool_calls = response['message']['tool_calls']

            if tool_calls:
                print("Agent: Wykryto wywołanie narzędzia...")
                for tool_call in tool_calls:
                    tool_name = tool_call['function']['name']
                    tool_args = json.loads(tool_call['function']['arguments'])

                    # Znajdź i wykonaj odpowiednie narzędzie
                    found_tool = next((t for t in ALL_TOOLS if t['function'].__name__ == tool_name), None)
                    if found_tool:
                        print(f"Agent: Wywołuję narzędzie {tool_name} z argumentami {tool_args}")
                        # Przekazujemy canister_id, jeśli narzędzie go potrzebuje
                        # Na razie hardkodujemy, w przyszłości można to zrobić konfigurowalne
                        canister_id = "uxrrr-q7777-77774-qaaaq-cai" # Przykład ID kanistra glue-testapp-backend
                        tool_result = await found_tool['function'](found_tool['input_model'](**tool_args), settings, canister_id)
                        print(f"Wynik narzędzia {tool_name}: {tool_result}")

                        # Dodaj wynik narzędzia do wiadomości i wywołaj LLM ponownie
                        messages.append({
                            "tool_call_id": tool_call.get('id'), # Bezpieczniejszy dostęp; OpenAI wymaga tool_call_id
                            "role": "tool",
                            "name": tool_name,
                            "content": json.dumps(tool_result)
                        })
                        final_response = await llm_client(user_input, settings, llm_tools) # Ponowne wywołanie z wynikiem narzędzia
                        if settings.agent_mode == 'openai':
                            print(f"Agent: {final_response['choices'][0]['message']['content']}")
                        elif settings.agent_mode == 'ollama':
                            print(f"Agent: {final_response['message']['content']}")
                    else:
                        print(f"Agent: Nie znaleziono narzędzia: {tool_name}")
            else:
                # Jeśli LLM nie wywołał narzędzia, wyświetl jego odpowiedź
                if settings.agent_mode == 'openai':
                    print(f"Agent: {response['choices'][0]['message']['content']}")
                elif settings.agent_mode == 'ollama':
                    print(f"Agent: {response['message']['content']}")

        except Exception as e:
            print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    asyncio.run(main())