import os
from fastmcp import Client, ToolError, ResourceError, McpError

class MCPClientWrapper:
    """
    Adapter do komunikacji z serwerem MCP (Model Context Protocol).
    """

    def __init__(self, server_url: str = ""):
        # Domyślny adres serwera MCP ustawiony na https://mcp.deepwiki.com/sse
        self.server_url = server_url or os.getenv("MCP_SERVER_URL") or "https://mcp.deepwiki.com/sse"
        self.client = Client(self.server_url)

    async def call_tool(self, tool_name: str, args: dict):
        async with self.client:
            return await self.client.call_tool(tool_name, args)

    async def read_resource(self, uri: str):
        async with self.client:
            return await self.client.read_resource(uri)

    async def get_prompt(self, prompt_name: str, args: dict):
        async with self.client:
            return await self.client.get_prompt(prompt_name, args)

    async def list_tools(self):
        async with self.client:
            return await self.client.list_tools()

    async def list_resources(self):
        async with self.client:
            return await self.client.list_resources()

    async def list_prompts(self):
        async with self.client:
            return await self.client.list_prompts()
