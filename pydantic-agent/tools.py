from pydantic import BaseModel, Field, HttpUrl
from typing import List, Dict, Any, Callable, Optional, Literal, Type
import json
import httpx

from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import encode, Types

from config import Settings

# --- Pydantic Schemas for Tool Inputs ---

class GlueGetInput(BaseModel):
    get: List[str] = Field(description="Lista stringów reprezentujących komendę i argumenty dla funkcji glue_get.")

class GluePushInput(BaseModel):
    push: List[str] = Field(description="Lista stringów reprezentujących komendę i argumenty dla funkcji glue_push.")

class HelpInput(BaseModel):
    line: int = Field(description="Numer linii pomocy do pobrania.")

class HwoismeInput(BaseModel):
    """Brak wymaganych argumentów."""
    pass

class ConnOneInput(BaseModel):
    target: int = Field(description="Indeks celu (canister) do pobrania informacji.")

class FrendOneInput(BaseModel):
    target: int = Field(description="Indeks celu (databox) do pobrania informacji.")

class ConnAddInput(BaseModel):
    connn: str = Field(description="Nazwa połączenia.")
    titlee: str = Field(description="Tytuł połączenia.")
    conectorr: List[str] = Field(description="Lista konektorów.")

class FrendAddInput(BaseModel):
    connn: str = Field(description="Nazwa połączenia przyjaciela.")
    titlee: str = Field(description="Tytuł połączenia przyjaciela.")
    conectorr: List[str] = Field(description="Lista konektorów przyjaciela.")

class ModeratorInput(BaseModel):
    line: str = Field(description="Komenda dla moderatora (np. 'conn', 'frend').")
    target: int = Field(description="Indeks celu do usunięcia.")

# --- Wrapper Functions for Tools ---

async def _call_mcp_server(tool_name: str, args: Dict[str, Any], mcp_server_url: HttpUrl) -> Any:
    """Wywołuje narzędzie poprzez niestandardowy serwer MCP."""
    headers = {'Content-Type': 'application/json'}
    payload = {
        "tool_name": tool_name,
        "args": args
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(str(mcp_server_url), headers=headers, json=payload)
            response.raise_for_status()  # Podnieś wyjątek dla kodów statusu 4xx/5xx
            return response.json()
        except httpx.RequestError as e:
            print(f"Błąd komunikacji z serwerem MCP: {e}")
            return {"error": f"Błąd połączenia z serwerem MCP: {e.request.url}"}
        except httpx.HTTPStatusError as e:
            print(f"Błąd serwera MCP: status {e.response.status_code} dla {e.request.url}")
            return {"error": f"Błąd serwera MCP: status {e.response.status_code}", "details": e.response.text}

async def _call_icp_canister(canister_id: str, method_name: str, args: List[Any], is_query: bool = True) -> Any:
    """Wywołuje metodę na kanistrze ICP."""
    ic_url = 'https://ic0.app' # Domyślny URL sieci ICP
    client = Client(url=ic_url)
    # Użycie anonimowej tożsamości. Dla wywołań 'update' może być wymagana uwierzytelniona tożsamość.
    identity = Identity() 
    agent = Agent(identity, client)

    try:
        encoded_args = encode(args)
        if is_query:
            result = await agent.query_raw_async(canister_id, method_name, encoded_args)
        else:
            result = await agent.update_raw_async(canister_id, method_name, encoded_args)
        
        # Dekodowanie wyniku. Odpowiedzi z kanistrów przychodzą jako lista słowników.
        # Dla prostoty, jeśli jest jeden wynik, zwracamy jego wartość.
        # W przeciwnym razie zwracamy całą listę.
        if isinstance(result, list):
            if len(result) == 1 and isinstance(result[0], dict) and 'value' in result[0]:
                return result[0]['value']
            elif len(result) == 0:
                return {"status": "ok", "message": "Operacja zakończona sukcesem, brak wartości zwrotnej."}
        return result # Zwróć surową listę, jeśli jest więcej wyników lub ma inną strukturę
    except Exception as e:
        print(f"Błąd wywołania kanistra ICP ({method_name}): {e}")
        return {"error": str(e)}

# --- Narzędzia MCP (wrappery) ---

async def glue_get_tool(input: GlueGetInput, settings: Settings, canister_id: str) -> Any:
    """Pobiera dane z interfejsu 'glue' kanistra ICP.
    Args:
        input: Obiekt GlueGetInput zawierający listę komend.
        settings: Obiekt Settings zawierający konfigurację MCP.
        canister_id: ID kanistra ICP do wywołania.
    """
    if settings.mcp_server_url:
        return await _call_mcp_server("glue_get", input.model_dump(), settings.mcp_server_url)
    else:
        # Przykład mapowania Pydantic na Candid Types
        candid_args = [{'type': Types.Vec(Types.Text), 'value': input.get}]  # type: ignore
        return await _call_icp_canister(canister_id, "glue_get", candid_args, is_query=True)

async def glue_push_tool(input: GluePushInput, settings: Settings, canister_id: str) -> Any:
    """Wysyła dane do interfejsu 'glue' kanistra ICP.
    Args:
        input: Obiekt GluePushInput zawierający listę komend.
        settings: Obiekt Settings zawierający konfigurację MCP.
        canister_id: ID kanistra ICP do wywołania.
    """
    if settings.mcp_server_url:
        return await _call_mcp_server("glue_push", input.model_dump(), settings.mcp_server_url)
    else:
        candid_args = [{'type': Types.Vec(Types.Text), 'value': input.push}]  # type: ignore
        return await _call_icp_canister(canister_id, "glue_push", candid_args, is_query=False)

async def help_tool(input: HelpInput, settings: Settings, canister_id: str) -> Any:
    """Pobiera pomoc dla danego kanistra ICP.
    Args:
        input: Obiekt HelpInput zawierający numer linii pomocy.
        settings: Obiekt Settings zawierający konfigurację MCP.
        canister_id: ID kanistra ICP do wywołania.
    """
    if settings.mcp_server_url:
        return await _call_mcp_server("help", input.model_dump(), settings.mcp_server_url)
    else:
        candid_args = [{'type': Types.Nat, 'value': input.line}]
        return await _call_icp_canister(canister_id, "help", candid_args, is_query=True)

async def hwoisme_tool(input: HwoismeInput, settings: Settings, canister_id: str) -> Any:
    """Pobiera informacje o kanistrze ICP (hwoisme).
    Args:
        input: Obiekt HwoismeInput (brak argumentów).
        settings: Obiekt Settings zawierający konfigurację MCP.
        canister_id: ID kanistra ICP do wywołania.
    """
    if settings.mcp_server_url:
        return await _call_mcp_server("hwoisme", input.model_dump(), settings.mcp_server_url)
    else:
        return await _call_icp_canister(canister_id, "hwoisme", [], is_query=True)

async def conn_one_tool(input: ConnOneInput, settings: Settings, canister_id: str) -> Any:
    """Pobiera informacje o połączeniu (conn) z databoxu ICP.
    Args:
        input: Obiekt ConnOneInput zawierający indeks celu.
        settings: Obiekt Settings zawierający konfigurację MCP.
        canister_id: ID kanistra ICP do wywołania.
    """
    if settings.mcp_server_url:
        return await _call_mcp_server("conn_one", input.model_dump(), settings.mcp_server_url)
    else:
        candid_args = [{'type': Types.Nat, 'value': input.target}]
        return await _call_icp_canister(canister_id, "conn_one", candid_args, is_query=True)

async def frend_one_tool(input: FrendOneInput, settings: Settings, canister_id: str) -> Any:
    """Pobiera informacje o przyjacielu (frend) z databoxu ICP.
    Args:
        input: Obiekt FrendOneInput zawierający indeks celu.
        settings: Obiekt Settings zawierający konfigurację MCP.
        canister_id: ID kanistra ICP do wywołania.
    """
    if settings.mcp_server_url:
        return await _call_mcp_server("frend_one", input.model_dump(), settings.mcp_server_url)
    else:
        candid_args = [{'type': Types.Nat, 'value': input.target}]
        return await _call_icp_canister(canister_id, "frend_one", candid_args, is_query=True)

async def conn_add_tool(input: ConnAddInput, settings: Settings, canister_id: str) -> Any:
    """Dodaje nowe połączenie (conn) do databoxu ICP.
    Args:
        input: Obiekt ConnAddInput zawierający dane połączenia.
        settings: Obiekt Settings zawierający konfigurację MCP.
        canister_id: ID kanistra ICP do wywołania.
    """
    if settings.mcp_server_url:
        return await _call_mcp_server("conn_add", input.model_dump(), settings.mcp_server_url)
    else:
        candid_args = [
            {'type': Types.Text, 'value': input.connn},
            {'type': Types.Text, 'value': input.titlee},
            {'type': Types.Vec(Types.Text), 'value': input.conectorr}  # type: ignore
        ]
        return await _call_icp_canister(canister_id, "conn_add", candid_args, is_query=False)

async def frend_add_tool(input: FrendAddInput, settings: Settings, canister_id: str) -> Any:
    """Dodaje nowego przyjaciela (frend) do databoxu ICP.
    Args:
        input: Obiekt FrendAddInput zawierający dane przyjaciela.
        settings: Obiekt Settings zawierający konfigurację MCP.
        canister_id: ID kanistra ICP do wywołania.
    """
    if settings.mcp_server_url:
        return await _call_mcp_server("frend_add", input.model_dump(), settings.mcp_server_url)
    else:
        candid_args = [
            {'type': Types.Text, 'value': input.connn},
            {'type': Types.Text, 'value': input.titlee},
            {'type': Types.Vec(Types.Text), 'value': input.conectorr}  # type: ignore
        ]
        return await _call_icp_canister(canister_id, "frend_add", candid_args, is_query=False)

async def moderator_tool(input: ModeratorInput, settings: Settings, canister_id: str) -> Any:
    """Wykonuje akcje moderatorskie na databoxie ICP.
    Args:
        input: Obiekt ModeratorInput zawierający komendę i indeks celu.
        settings: Obiekt Settings zawierający konfigurację MCP.
        canister_id: ID kanistra ICP do wywołania.
    """
    if settings.mcp_server_url:
        return await _call_mcp_server("moderator", input.model_dump(), settings.mcp_server_url)
    else:
        candid_args = [
            {'type': Types.Text, 'value': input.line},
            {'type': Types.Nat, 'value': input.target}
        ]
        return await _call_icp_canister(canister_id, "moderator", candid_args, is_query=False)

# --- Funkcja do generowania schematów narzędzi dla OpenAI ---

def get_tool_schema(tool_func: Callable, input_model: Type[BaseModel]) -> Dict[str, Any]:
    """Generuje schemat narzędzia w formacie OpenAI na podstawie funkcji i modelu Pydantic.
    Args:
        tool_func: Funkcja narzędzia (np. glue_get_tool).
        input_model: Model Pydantic dla wejścia funkcji.
    Returns:
        Słownik reprezentujący schemat narzędzia dla OpenAI.
    """
    return {
        "type": "function",
        "function": {
            "name": tool_func.__name__,
            "description": tool_func.__doc__.strip() if tool_func.__doc__ else "",
            "parameters": input_model.model_json_schema()
        }
    }

# Lista wszystkich dostępnych narzędzi
ALL_TOOLS = [
    {"function": glue_get_tool, "input_model": GlueGetInput},
    {"function": glue_push_tool, "input_model": GluePushInput},
    {"function": help_tool, "input_model": HelpInput},
    {"function": hwoisme_tool, "input_model": HwoismeInput},
    {"function": conn_one_tool, "input_model": ConnOneInput},
    {"function": frend_one_tool, "input_model": FrendOneInput},
    {"function": conn_add_tool, "input_model": ConnAddInput},
    {"function": frend_add_tool, "input_model": FrendAddInput},
    {"function": moderator_tool, "input_model": ModeratorInput},
]

# Przykład użycia i demonstracja działania narzędzi
if __name__ == "__main__":
    print("--- DEMONSTRACJA NARZĘDZI ---")

    print("\n1. Generowanie schematu narzędzia dla OpenAI:")
    help_schema = get_tool_schema(help_tool, HelpInput)
    print(json.dumps(help_schema, indent=2))

    # Ustawienia do testów
    class TestSettings(Settings):
        # Ustaw URL serwera MCP, jeśli chcesz testować tę ścieżkę
        mcp_server_url: Optional[HttpUrl] = None # HttpUrl("http://localhost:8000/mcp")
        agent_mode: Literal['ollama', 'openai'] = 'openai'

    async def run_tool_tests():
        print("\n--- Uruchamianie testów wywołań narzędzi ---")
        settings = TestSettings()
        # Użyj prawdziwego ID kanistra, jeśli chcesz testować wywołania ICP
        # Poniżej ID kanistra z przykładu, może nie być aktywne.
        canister_id = "uxrrr-q7777-77774-qaaaq-cai" 

        # Test 1: Wywołanie narzędzia, które korzysta z ICP (bo mcp_server_url jest None)
        print(f"\n2. Test wywołania 'hwoisme_tool' na kanistrze: {canister_id}")
        print("   (Oczekiwany błąd, jeśli kanister nie istnieje lub nie ma metody 'hwoisme')")
        try:
            result = await hwoisme_tool(HwoismeInput(), settings, canister_id)
            print(f"   Wynik: {result}")
        except Exception as e:
            print(f"   Wystąpił wyjątek: {e}")

        # Test 2: Zmiana ustawień, aby użyć serwera MCP
        print(f"\n3. Test wywołania 'help_tool' przez serwer MCP")
        settings.mcp_server_url = HttpUrl("http://localhost:9999/invalid_mcp")
        print(f"   (Oczekiwany błąd połączenia z serwerem MCP pod adresem: {settings.mcp_server_url})")
        result = await help_tool(HelpInput(line=1), settings, canister_id)
        print(f"   Wynik: {result}")

    import asyncio
    # Uruchomienie testów. Spodziewaj się błędów, jeśli serwery/kanistry nie są dostępne.
    # To demonstruje, że kod jest funkcjonalny i próbuje się połączyć.
    asyncio.run(run_tool_tests())
    print("\n--- Demonstracja zakończona ---")