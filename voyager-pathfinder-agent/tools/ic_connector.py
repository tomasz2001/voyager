import asyncio
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import encode, Types


class ICConnector:
    def __init__(self, canister_id='p2137-cai', agent=None):
        self.canister_id = canister_id
        if agent:
            self.agent = agent
        else:
            self.agent = self._create_agent()


    def _create_agent(self):
        ic_url = 'https://ic0.app'
        client = Client(url=ic_url)
        identity = Identity()
        return Agent(identity, client)


    async def set_canister_id(self, canister_id: str):
        """Sets the target canister ID for communication."""
        self.canister_id = canister_id
        return f"Canister ID set to: {self.canister_id}"


    async def _execute_ic_call(self, method_name, params):
        try:
            if method_name in ["glue_push"]:
                 # Update call for methods that change state
                result = await self.agent.update_raw_async(self.canister_id, method_name, encode(params))
            else:
                # Query call for read-only methods
                result = await self.agent.query_raw_async(self.canister_id, method_name, encode(params))
            
            if isinstance(result, list) and len(result) > 0 and 'value' in result[0]:
                return result[0]['value']
            elif isinstance(result, str):
                return result
            else:
                return f"Error: Unexpected response format from IC: {result}"
        except Exception as e:
            return f"Error during IC call: {e}"


    async def hwoisme(self) -> dict | str:
        """Checks who the agent is talking to and what interfaces it has."""
        return await self._execute_ic_call("hwoisme", [])


    async def get_app(self, index: int) -> dict | str:
        """Fetches information about a specific application by its index."""
        params = [{'type': Types.Nat, 'value': index}]
        return await self._execute_ic_call("conn_one", params)


    async def get_box(self, index: int) -> dict | str:
        """Fetches information about a specific databox by its index."""
        params = [{'type': Types.Nat, 'value': index}]
        return await self._execute_ic_call("frend_one", params)


    async def use_glue_get(self, data: list[str]) -> str:
        """Uses the 'glue_get' interface with the selected target."""
        # Rozwiązanie 1: Używanie Types.text zamiast Types.Text
        params = [{'type': Types.Vec(Types.text), 'value': data}]
        return await self._execute_ic_call("glue_get", params)
    
    async def use_glue_push(self, data: list[str]) -> str:
        """Uses the 'glue_push' interface with the selected target to push data."""
        # Rozwiązanie 1: Używanie Types.text zamiast Types.Text
        params = [{'type': Types.Vec(Types.text), 'value': data}]
        return await self._execute_ic_call("glue_push", params)


    async def get_help(self, page: int) -> str:
        """Gets the help page from the service."""
        params = [{'type': Types.Nat, 'value': page}]
        return await self._execute_ic_call("help", params)
