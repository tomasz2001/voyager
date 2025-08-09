from voyager_py_agent_panda.ic_connector import ICConnector
from voyager_py_agent_panda.voyager_agent import VoyagerAgent
from dataclasses import dataclass
from typing import List
import asyncio

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
    def __init__(self, ic_connector: ICConnector):
        self.ic_connector = ic_connector
        self.agent = VoyagerAgent(ic_connector)
        self.databox_canister_id = None
        print("VoyagerConnector initialized with ICConnector and VoyagerAgent.")

    def connect_to_databox(self, databox_principal_id: str):
        self.databox_canister_id = databox_principal_id
        print(f"Connected to DataBox: {self.databox_canister_id}")

    async def call_databox_method(self, method_name: str, *args):
        if not self.databox_canister_id:
            raise Exception("Not connected to a DataBox. Call connect_to_databox first.")
        # Assuming the VoyagerAgent's call_canister_method can handle the arguments directly
        return await self.agent.call_canister_method(self.databox_canister_id, method_name, *args)

    async def get_databox_help(self, line: int) -> str:
        response = await self.call_databox_method("help", line)
        # Assuming the response from Motoko's Text type is directly usable as a string
        return response

    async def get_databox_hwoisme(self) -> Conn:
        response = await self.call_databox_method("hwoisme")
        # Assuming the response is a dictionary that matches the Conn dataclass structure
        return Conn(**response)

    async def get_databox_frend_one(self, index: int) -> Voyager:
        response = await self.call_databox_method("frend_one", index)
        # Assuming the response is a dictionary that matches the Voyager dataclass structure
        return Voyager(**response)

    async def get_databox_conn_one(self, index: int) -> Conn:
        response = await self.call_databox_method("conn_one", index)
        # Assuming the response is a dictionary that matches the Conn dataclass structure
        return Conn(**response)

    async def add_databox_frend(self, conn: str, title: str, conector: List[str]) -> str:
        response = await self.call_databox_method("frend_add", conn, title, conector)
        return response

    async def add_databox_conn(self, conn: str, title: str, conector: List[str]) -> str:
        response = await self.call_databox_method("conn_add", conn, title, conector)
        return response

    async def databox_moderator(self, line: str, target: int) -> str:
        response = await self.call_databox_method("moderator", line, target)
        return response

    async def call_app_method(self, app_canister_id: str, method_name: str, *args):
        # This method allows calling any method on an app canister
        return await self.agent.call_canister_method(app_canister_id, method_name, *args)
