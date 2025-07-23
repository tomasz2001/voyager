import ollama
import openai
from typing import List, Dict, Any, Callable, Awaitable
from config import Settings, OllamaSettings, OpenAISettings

async def get_ollama_response(
    prompt: str,
    settings: OllamaSettings,
    tools: List[Dict[str, Any]] = []
) -> Dict[str, Any]:
    """Pobiera odpowiedź z modelu Ollama, z opcjonalnym wsparciem dla narzędzi.

    Args:
        prompt: Treść zapytania do modelu.
        settings: Ustawienia konfiguracji Ollama.
        tools: Lista definicji narzędzi w formacie Ollama (Python function).

    Returns:
        Słownik zawierający odpowiedź modelu, w tym ewentualne wywołania narzędzi.
    """
    messages = [{'role': 'user', 'content': prompt}]
    
    # Ollama automatycznie generuje schemat narzędzia z funkcji Pythona
    # więc przekazujemy listę funkcji, a nie JSON Schema
    ollama_tools = []
    for tool_def in tools:
        # Zakładamy, że tool_def to słownik z kluczem 'function' zawierającym callable
        if 'function' in tool_def and callable(tool_def['function']):
            ollama_tools.append(tool_def['function'])

    # Używamy AsyncClient dla operacji asynchronicznych, zgodnie z dokumentacją biblioteki.
    client = ollama.AsyncClient()
    response = await client.chat(
        model=settings.model_name,
        messages=messages,
        tools=ollama_tools,
        stream=False # Dla prostoty, nie używamy streamingu w tym demo
    )
    # Zwracamy słownik dla spójności z klientem OpenAI.
    # ChatResponse to TypedDict, który jest już słownikiem, ale to upewnia typy.
    return dict(response)

async def get_openai_response(
    prompt: str,
    settings: OpenAISettings,
    tools: List[Dict[str, Any]] = []
) -> Dict[str, Any]:
    """Pobiera odpowiedź z modelu kompatybilnego z OpenAI API, z opcjonalnym wsparciem dla narzędzi.

    Args:
        prompt: Treść zapytania do modelu.
        settings: Ustawienia konfiguracji OpenAI.
        tools: Lista definicji narzędzi w formacie JSON Schema.

    Returns:
        Słownik zawierający odpowiedź modelu, w tym ewentualne wywołania narzędzi.
    """
    # Walidator w Settings zapewnia, że api_key nie jest None w trybie 'openai'.
    # Ten assert pomaga statycznemu analizatorowi kodu to zrozumieć.
    assert settings.api_key, "OpenAI API key is required but was not found."
    client = openai.AsyncOpenAI(
        api_key=settings.api_key.get_secret_value(),
        base_url=str(settings.base_url) if settings.base_url else None,
        organization=settings.organization
    )
    messages = [{'role': 'user', 'content': prompt}]

    # Biblioteka openai używa bardzo ścisłych typów (TypedDict), które nie pasują do
    # generycznych słowników, mimo że struktura jest poprawna w czasie wykonania.
    # Używamy openai.NOT_GIVEN zamiast None dla opcjonalnych parametrów.
    response = await client.chat.completions.create(
        model="gpt-4o", # Można to zrobić konfigurowalne w przyszłości
        messages=messages, # type: ignore
        tools=tools if tools else openai.NOT_GIVEN, # type: ignore
        tool_choice="auto", # Pozwól modelowi zdecydować, czy użyć narzędzia
        stream=False
    )
    return response.model_dump() # Zwracamy słownik dla spójności

def get_llm_client(
    settings: Settings
) -> Callable[[str, Any, List[Dict[str, Any]]], Awaitable[Dict[str, Any]]]:
    """Zwraca odpowiednią funkcję klienta LLM na podstawie konfiguracji.

    Args:
        settings: Obiekt konfiguracji agenta.

    Returns:
        Asynchroniczna funkcja klienta LLM.

    Raises:
        ValueError: Jeśli AGENT_MODE jest nieprawidłowy.
    """
    if settings.agent_mode == 'ollama':
        return lambda p, s, t: get_ollama_response(p, settings.ollama, t)
    elif settings.agent_mode == 'openai':
        return lambda p, s, t: get_openai_response(p, settings.openai, t)
    else:
        raise ValueError(f"Nieznany tryb agenta: {settings.agent_mode}")

# Przykład użycia (dla celów testowych, można usunąć w finalnej wersji)
if __name__ == "__main__":
    import asyncio
    import os
    from dotenv import load_dotenv

    load_dotenv(dotenv_path='G:/Backup lapek/GEMINI/aiagent/voyager/pydantic-agent/.env')

    # Test Ollama
    os.environ['AGENT_MODE'] = 'ollama'
    os.environ['OLLAMA_MODEL'] = 'llama3' # Upewnij się, że masz ten model pobrany lokalnie
    try:
        settings = Settings()
        ollama_client_func = get_llm_client(settings)
        print("Testowanie Ollama...")
        # response = asyncio.run(ollama_client_func("Powiedz mi coś o Pythonie.", settings.ollama, []))
        # print(f"Ollama Response: {response}")
        print("Test Ollama zakończony (zakomentowany, aby nie wywoływać LLM za każdym razem).")
    except Exception as e:
        print(f"Błąd podczas testowania Ollama: {e}")

    # Test OpenAI
    os.environ['AGENT_MODE'] = 'openai'
    os.environ['OPENAI_API_KEY'] = 'sk-test-key-123' # Zastąp prawdziwym kluczem dla testów
    os.environ['OPENAI_BASE_URL'] = 'https://api.openai.com/v1'
    try:
        settings = Settings()
        openai_client_func = get_llm_client(settings)
        print("\nTestowanie OpenAI...")
        # response = asyncio.run(openai_client_func("Powiedz mi coś o sztucznej inteligencji.", settings.openai, []))
        # print(f"OpenAI Response: {response}")
        print("Test OpenAI zakończony (zakomentowany, aby nie wywoływać LLM za każdym razem).")
    except Exception as e:
        print(f"Błąd podczas testowania OpenAI: {e}")