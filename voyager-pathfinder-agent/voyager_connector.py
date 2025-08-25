from ic.agent import Agent
from ic.candid import encode, decode, Types
from dataclasses import dataclass
from typing import List, Any

# Definicje struktur danych, które są zwracane przez kanistry
@dataclass
class Conn:
    conn: str
    title: str
    conector: List[str]

@dataclass
class Voyager:
    conn: str
    title: str
    conector: List[str]

class VoyagerConnector:
    def __init__(self, agent: Agent):
        """Inicjalizuje konektor bezpośrednio z agentem ic-py."""
        self.agent = agent
        self.databox_canister_id = None
        print("VoyagerConnector initialized with a direct ic-py Agent.")

    def connect_to_databox(self, databox_principal_id: str):
        """Ustawia ID kanistra DataBox, z którym będziemy się komunikować."""
        self.databox_canister_id = databox_principal_id
        print(f"VoyagerConnector is now connected to DataBox: {self.databox_canister_id}")

    async def _call_canister(self, canister_id: str, method_name: str, args: list, out_types: list) -> Any:
        """Prywatna, generyczna metoda do wywoływania funkcji na dowolnym kanistrze."""
        encoded_args = encode(args)
        
        is_update_call = "add" in method_name or "push" in method_name or "moderator" in method_name
        
        try:
            if is_update_call:
                print(f"Executing UPDATE call: {canister_id}.{method_name}")
                response = await self.agent.update_raw_async(canister_id, method_name, encoded_args)
            else:
                print(f"Executing QUERY call: {canister_id}.{method_name}")
                response = await self.agent.query_raw_async(canister_id, method_name, encoded_args)
        except Exception as e:
            print(f"Exception during IC call to {canister_id}.{method_name}: {e}")
            raise e

        if isinstance(response, list) and len(response) > 0 and isinstance(response[0], dict) and 'value' in response[0]:
            return response[0]['value']
        else:
            raise TypeError(f"Unexpected response format from canister: {response}")

    # --- Metody specyficzne dla DataBoxa ---

    async def call_databox_method(self, method_name: str, args: list, out_types: list) -> Any:
        """Wywołuje metodę na podłączonym kanistrze DataBox."""
        if not self.databox_canister_id:
            raise Exception("Not connected to a DataBox. Call connect_to_databox first.")
        return await self._call_canister(self.databox_canister_id, method_name, args, out_types)

    async def get_databox_help(self, line: int) -> str:
        args = [{'type': Types.Nat, 'value': int(line)}]
        out_types = [Types.Text]
        return await self.call_databox_method("help", args, out_types)

    async def get_databox_hwoisme(self) -> Conn:
        args = []
        out_types = [Types.Record({'conn': Types.Text, 'title': Types.Text, 'conector': Types.Vec(Types.Text)})]
        response_dict = await self.call_databox_method("hwoisme", args, out_types)
        values = list(response_dict.values())
        return Conn(title=values[0], conn=values[1], conector=values[2])

    async def get_databox_frend_one(self, index: int) -> Voyager:
        args = [{'type': Types.Nat, 'value': int(index)}]
        out_types = [Types.Record({'conn': Types.Text, 'title': Types.Text, 'conector': Types.Vec(Types.Text)})]
        response_dict = await self.call_databox_method("frend_one", args, out_types)
        values = list(response_dict.values())
        return Voyager(title=values[0], conn=values[1], conector=values[2])

    async def get_databox_conn_one(self, index: int) -> Conn:
        args = [{'type': Types.Nat, 'value': int(index)}]
        out_types = [Types.Record({'conn': Types.Text, 'title': Types.Text, 'conector': Types.Vec(Types.Text)})]
        response_dict = await self.call_databox_method("conn_one", args, out_types)
        # Ręczne mapowanie pól, ponieważ kanister zwraca nienazwane pola (hashe)
        values = list(response_dict.values())
        return Conn(title=values[0], conn=values[1], conector=values[2])

    # --- Metoda generyczna dla Aplikacji ---

    async def call_app_method(self, app_canister_id: str, method_name: str, *args) -> Any:
        """Wywołuje dowolną metodę na dowolnym kanistrze aplikacji."""
        print(f"Generic call to {app_canister_id}.{method_name} with args: {args}")
        
        def guess_type(value):
            if isinstance(value, str): return Types.Text
            if isinstance(value, int): return Types.Nat
            if isinstance(value, list): return Types.Vec(Types.Text)
            return Types.Text

        candid_args = [{'type': guess_type(arg), 'value': arg} for arg in args]
        
        try:
            # Zakładamy, że większość zwraca tekst dla prostoty
            return await self._call_canister(app_canister_id, method_name, candid_args, [Types.Text])
        except Exception as e:
            print(f"Error during generic app method call: {e}")
            raise e # Rzucamy wyjątek dalej, zamiast zwracać string