from pydantic import Field, HttpUrl, SecretStr, ValidationError, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, Optional, Union

class OllamaSettings(BaseSettings):
    model_name: str = "llama3"

class OpenAISettings(BaseSettings):
    api_key: Optional[SecretStr] = None
    base_url: Optional[HttpUrl] = None
    organization: Optional[str] = None

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    agent_mode: Literal['ollama', 'openai'] = 'ollama'
    ollama: OllamaSettings = Field(default_factory=OllamaSettings)
    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    mcp_server_url: Optional[HttpUrl] = None

    @model_validator(mode='after')
    def _check_settings(self):
        if self.agent_mode == 'openai':
            if not self.openai.api_key or not self.openai.api_key.get_secret_value():
                raise ValueError("OPENAI_API_KEY must be set for openai agent_mode")
        return self

# Przykład użycia (dla celów testowych, można usunąć w finalnej wersji)
if __name__ == "__main__":
    import os
    # Ustawienie zmiennych środowiskowych dla testów
    os.environ['AGENT_MODE'] = 'ollama'
    os.environ['OLLAMA_MODEL'] = 'mistral'
    os.environ['OPENAI_API_KEY'] = 'sk-test-key' # To powinno być ignorowane w trybie ollama

    try:
        settings = Settings()
        print("Konfiguracja Ollama:")
        print(f"Agent Mode: {settings.agent_mode}")
        print(f"Ollama Model: {settings.ollama.model_name}")
        print(f"MCP Server URL: {settings.mcp_server_url}")
        print("-" * 30)
    except ValidationError as e:
        print(f"Błąd walidacji konfiguracji Ollama: {e}")

    os.environ['AGENT_MODE'] = 'openai'
    os.environ['OPENAI_API_KEY'] = 'sk-prod-key-123'
    os.environ['OPENAI_BASE_URL'] = 'https://api.openai.com/v1'
    os.environ['OPENAI_ORGANIZATION'] = 'org-xyz'
    os.environ['MCP_SERVER_URL'] = 'http://localhost:8000/mcp'

    try:
        settings = Settings()
        print("Konfiguracja OpenAI:")
        print(f"Agent Mode: {settings.agent_mode}")
        if settings.openai.api_key:
            print(f"OpenAI API Key: {settings.openai.api_key.get_secret_value()}")
        print(f"OpenAI Base URL: {settings.openai.base_url}")
        print(f"OpenAI Organization: {settings.openai.organization}")
        print(f"MCP Server URL: {settings.mcp_server_url}")
    except ValidationError as e:
        print(f"Błąd walidacji konfiguracji OpenAI: {e}")

    # Test błędu dla trybu openai bez klucza
    del os.environ['OPENAI_API_KEY']
    try:
        os.environ['AGENT_MODE'] = 'openai'
        settings = Settings()
    except ValidationError as e:
        print("-" * 30)
        print(f"Oczekiwany błąd walidacji (brak klucza OpenAI): {e}")
