import asyncio
from pathlib import Path
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import encode, Types, decode

# Stała przechowująca ID kanistra vmessage
VMESSAGE_CANISTER_ID = "bkxiq-haaaa-aaaad-abo5q-cai"

class VMessageConnector:
    """
    Klasa konektora do obsługi komunikacji z kanistrem vmessage w sieci IC.
    """
    def __init__(self, identity_path: Path):
        """
        Inicjalizuje konektor, tworząc agenta z podaną tożsamością.

        :param identity_path: Ścieżka do pliku identity.pem.
        """
        self.canister_id = VMESSAGE_CANISTER_ID
        self.agent = self._create_agent(identity_path)
        self.principal = self.agent.get_principal()

    def _create_agent(self, pem_path: Path) -> Agent:
        """
        Tworzy i zwraca agenta IC z tożsamością załadowaną z pliku PEM.
        Jeśli plik nie istnieje, tworzy nową tożsamość.
        """
        if pem_path.exists():
            print(f"INFO: Znaleziono istniejącą tożsamość w: {pem_path}")
            identity = Identity.from_pem(pem_path.read_text())
        else:
            print(f"INFO: Nie znaleziono tożsamości, tworzę nową w: {pem_path}")
            identity = Identity()
            pem_path.parent.mkdir(parents=True, exist_ok=True)
            pem_path.write_text(identity.to_pem())

        client = Client(url="https://ic0.app")
        return Agent(identity, client)

    async def _execute_call(self, method_type: str, method_name: str, params: list, out_types: list):
        """
        Prywatna metoda do wykonywania wywołań (query lub update) na kanistrze.
        """
        try:
            if method_type == 'update':
                result_raw = await self.agent.update_raw_async(self.canister_id, method_name, encode(params))
            else: # query
                result_raw = await self.agent.query_raw_async(self.canister_id, method_name, encode(params))
            
            # Dekodowanie odpowiedzi
            result_decoded = decode(result_raw, out_types)
            return result_decoded[0] if result_decoded else None

        except Exception as e:
            # Zwracamy błąd w ustandaryzowanym formacie
            return {"err": f"Błąd wywołania {method_name}: {e}"}

    def get_my_principal(self) -> str:
        """Zwraca Principal ID aktualnego agenta w formacie tekstowym."""
        return self.principal.to_str()

    async def hwoisme(self):
        """Sprawdza z kim rozmawia agent."""
        import asyncio
from pathlib import Path
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import encode, Types, decode

# Stała przechowująca ID kanistra vmessage
VMESSAGE_CANISTER_ID = "bkxiq-haaaa-aaaad-abo5q-cai"

class VMessageConnector:
    """
    Klasa konektora do obsługi komunikacji z kanistrem vmessage w sieci IC.
    """
    def __init__(self, identity_path: Path):
        """
        Inicjalizuje konektor, tworząc agenta z podaną tożsamością.

        :param identity_path: Ścieżka do pliku identity.pem.
        """
        self.canister_id = VMESSAGE_CANISTER_ID
        self.agent = self._create_agent(identity_path)
        self.principal = self.agent.get_principal()

    def _create_agent(self, pem_path: Path) -> Agent:
        """
        Tworzy i zwraca agenta IC z tożsamością załadowaną z pliku PEM.
        Jeśli plik nie istnieje, tworzy nową tożsamość.
        """
        if pem_path.exists():
            print(f"INFO: Znaleziono istniejącą tożsamość w: {pem_path}")
            identity = Identity.from_pem(pem_path.read_text())
        else:
            print(f"INFO: Nie znaleziono tożsamości, tworzę nową w: {pem_path}")
            identity = Identity()
            pem_path.parent.mkdir(parents=True, exist_ok=True)
            pem_path.write_text(identity.to_pem())

        client = Client(url="https://ic0.app")
        return Agent(identity, client)

    async def _execute_call(self, method_type: str, method_name: str, params: list, out_types: list):
        """
        Prywatna metoda do wykonywania wywołań (query lub update) na kanistrze.
        """
        try:
            if method_type == 'update':
                result_raw = await self.agent.update_raw_async(self.canister_id, method_name, encode(params))
            else: # query
                result_raw = await self.agent.query_raw_async(self.canister_id, method_name, encode(params))
            
            # Dekodowanie odpowiedzi
            result_decoded = decode(result_raw, out_types)
            return result_decoded[0] if result_decoded else None

        except Exception as e:
            # Zwracamy błąd w ustandaryzowanym formacie
            return {"err": f"Błąd wywołania {method_name}: {e}"}

    def get_my_principal(self) -> str:
        """Zwraca Principal ID aktualnego agenta w formacie tekstowym."""
        return self.principal.to_str()

    async def hwoisme(self):
        """Sprawdza z kim rozmawia agent."""
        return await self._execute_call(
            'query', 
            "hwoisme", 
            [], 
            [Types.Record({'conn': Types.Text, 'title': Types.Text, 'conector': Types.Vec(Types.Text)})]
        )

    async def get_help(self, page: int):
        """Pobiera stronę pomocy z kanistra."""
        params = [{'type': Types.Nat, 'value': page}]
        return await self._execute_call('query', "help", params, [Types.Text])

    async def send_message(self, recipient_principal: str, message: str):
        """Wysyła wiadomość do podanego odbiorcy."""
        params = [{'type': Types.Vec(Types.Text), 'value': ["say", recipient_principal, message]}]
        return await self._execute_call('update', "glue_push", params, [Types.Text])

    async def check_messages(self):
        """
        Sprawdza i odbiera wiadomości. Jest to proces dwuetapowy.
        """
        # Etap 1: Sprawdzenie, czy jest wiadomość
        check_params = [{'type': Types.Vec(Types.Text), 'value': ["watch"]}]
        check_result = await self._execute_call('query', "glue_get", check_params, [Types.Text])

        if isinstance(check_result, dict) and 'err' in check_result:
            return check_result # Zwróć błąd, jeśli wystąpił

        if check_result == "PUSH":
            # Etap 2: Odebranie wiadomości
            print("INFO: Wykryto nową wiadomość. Pobieranie...")
            fetch_params = [{'type': Types.Vec(Types.Text), 'value': ["watch"]}]
            return await self._execute_call('update', "glue_push", fetch_params, [Types.Text])
        else:
            return "Twoja skrzynka jest pusta."

    async def get_help(self, page: int):
        """Pobiera stronę pomocy z kanistra."""
        params = [{'type': Types.Nat, 'value': page}]
        return await self._execute_call('query', "help", params, [Types.Text])

    async def send_message(self, recipient_principal: str, message: str):
        """Wysyła wiadomość do podanego odbiorcy."""
        params = [{'type': Types.Vec(Types.Text), 'value': ["say", recipient_principal, message]}]
        return await self._execute_call('update', "glue_push", params, [Types.Text])

    async def check_messages(self):
        """
        Sprawdza i odbiera wiadomości. Jest to proces dwuetapowy.
        """
        # Etap 1: Sprawdzenie, czy jest wiadomość
        check_params = [{'type': Types.Vec(Types.Text), 'value': ["watch"]}]
        check_result = await self._execute_call('query', "glue_get", check_params, [Types.Text])

        if isinstance(check_result, dict) and 'err' in check_result:
            return check_result # Zwróć błąd, jeśli wystąpił

        if check_result == "PUSH":
            # Etap 2: Odebranie wiadomości
            print("INFO: Wykryto nową wiadomość. Pobieranie...")
            fetch_params = [{'type': Types.Vec(Types.Text), 'value': ["watch"]}]
            return await self._execute_call('update', "glue_push", fetch_params, [Types.Text])
        else:
            return "Twoja skrzynka jest pusta."