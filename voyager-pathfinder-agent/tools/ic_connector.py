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
        try:
            self.canister_id = canister_id
            return f"Canister ID set to: {self.canister_id}"
        except Exception as e:
            return f"Error in set_canister_id: {e}"


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
        try:
            return await self._execute_ic_call("hwoisme", [])
        except Exception as e:
            return f"Error in hwoisme: {e}"


    async def get_app(self, index: int) -> dict | str:
        """Fetches information about a specific application by its index."""
        try:
            params = [{'type': Types.Nat, 'value': index}]
            return await self._execute_ic_call("conn_one", params)
        except Exception as e:
            return f"Error in get_app: {e}"

    async def get_box(self, index: int) -> dict | str:
        """Fetches information about a specific databox by its index."""
        try:
            params = [{'type': Types.Nat, 'value': index}]
            return await self._execute_ic_call("frend_one", params)
        except Exception as e:
            return f"Error in get_box: {e}"


    async def use_glue_get(self, data: list[str]) -> str:
        """Uses the 'glue_get' interface with the selected target."""
        # Rozwiązanie 1: Używanie Types.text zamiast Types.Text
        try:
            params = [{'type': Types.Vec(Types.Text), 'value': data}]
            return await self._execute_ic_call("glue_get", params)
        except Exception as e:
            return f"Error in use_glue_get: {e}"
    
    async def use_glue_push(self, data: list[str]) -> str:
        """Uses the 'glue_push' interface with the selected target to push data."""
        # Rozwiązanie 1: Używanie Types.text zamiast Types.Text
        try:
            params = [{'type': Types.Vec(Types.Text), 'value': data}]
            return await self._execute_ic_call("glue_push", params)
        except Exception as e:
            return f"Error in use_glue_push: {e}"

    async def get_help(self, page: int) -> str:
        """Gets the help page from the service."""
        # Convert page to int, as it might be received as a string from the tool call
        try:
            page_int = int(page)
            params = [{'type': Types.Nat, 'value': page_int}]
            return await self._execute_ic_call("help", params)
        except Exception as e:
            return f"Error in get_help: {e}"


    async def get_help_all(self) -> str:
        """Retrieves all available help pages until an error is encountered."""
        all_help_content = []
        # Use a large range for the for loop, as the number of help pages is unknown
        # The loop will break when get_help returns an error or empty content
        for page in range(100): # Assuming a maximum of 100 help pages
            try:
                help_page_content = await self.get_help(page)
                # Check for specific "NULL" or empty content indicating end of help pages
                if help_page_content.startswith("Error:") or help_page_content.strip() == "NULL" or not help_page_content.strip():
                    break
                all_help_content.append(f"--- Help Page {page} ---\n{help_page_content}")
            except Exception as e:
                # Catch any other potential exceptions during the call
                all_help_content.append(f"--- Stopped at page {page} due to error: {e} ---")
                break
        if not all_help_content:
            return "No help content found or an immediate error occurred."
        return "\n".join(all_help_content)
