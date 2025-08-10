import ollama
import json
import asyncio
from ic_connector import ICConnector

class VoyagerAgent:
    def __init__(self, model="qwen3:1.7b"):
        self.model = model
        self.ic_connector = ICConnector()
        # Map tool names to their async methods
        self.tools = {
            "set_canister_id": self.ic_connector.set_canister_id,
            "hwoisme": self.ic_connector.hwoisme,
            "get_app": self.ic_connector.get_app,
            "get_box": self.ic_connector.get_box,
            "use_glue_get": self.ic_connector.use_glue_get,
            "use_glue_push": self.ic_connector.use_glue_push,
            "get_help": self.ic_connector.get_help,
        }
        self.history = []

    async def chat_with_tools(self, prompt: str):
        self.history.append({'role': 'user', 'content': prompt})

        while True:
            response = ollama.chat(
                model=self.model,
                messages=self.history,
                tools=[
                    {
                        'type': 'function',
                        'function': {
                            'name': 'set_canister_id',
                            'description': 'Sets the target canister ID for all subsequent communication.',
                            'parameters': {
                                'type': 'object',
                                'properties': {
                                    'canister_id': {
                                        'type': 'string',
                                        'description': 'The new canister ID to target.',
                                    },
                                },
                                'required': ['canister_id'],
                            },
                        },
                    },
                    {
                        'type': 'function',
                        'function': {
                            'name': 'hwoisme',
                            'description': 'Checks who the agent is talking to and what interfaces the canister has.',
                            'parameters': {'type': 'object', 'properties': {}},
                        },
                    },
                    {
                        'type': 'function',
                        'function': {
                            'name': 'get_app',
                            'description': 'Fetches information about a specific application (conn) by its index from the current databox.',
                            'parameters': {
                                'type': 'object',
                                'properties': {
                                    'index': {
                                        'type': 'integer',
                                        'description': 'The index of the application to fetch.',
                                    },
                                },
                                'required': ['index'],
                            },
                        },
                    },
                    {
                        'type': 'function',
                        'function': {
                            'name': 'get_box',
                            'description': 'Fetches information about a specific databox (frend) by its index from the current databox.',
                            'parameters': {
                                'type': 'object',
                                'properties': {
                                    'index': {
                                        'type': 'integer',
                                        'description': 'The index of the databox to fetch.',
                                    },
                                },
                                'required': ['index'],
                            },
                        },
                    },
                    {
                        'type': 'function',
                        'function': {
                            'name': 'use_glue_get',
                            'description': "Uses the 'glue_get' interface with the selected target. Typically used to read data, like posts.",
                            'parameters': {
                                'type': 'object',
                                'properties': {
                                    'data': {
                                        'type': 'array',
                                        'items': {'type': 'string'},
                                        'description': "A list of strings, where the first is the command (e.g., 'watch') and subsequent are arguments (e.g., post number).",
                                    },
                                },
                                'required': ['data'],
                            },
                        },
                    },
                    {
                        'type': 'function',
                        'function': {
                            'name': 'use_glue_push',
                            'description': "Uses the 'glue_push' interface to send data to the target. Typically used to create new content, like posts.",
                            'parameters': {
                                'type': 'object',
                                'properties': {
                                    'data': {
                                        'type': 'array',
                                        'items': {'type': 'string'},
                                        'description': "A list of strings, where the first is the command (e.g., 'post') and subsequent are arguments (e.g., nick, content).",
                                    },
                                },
                                'required': ['data'],
                            },
                        },
                    },
                    {
                        'type': 'function',
                        'function': {
                            'name': 'get_help',
                            'description': 'Gets a specific help page from the service canister.',
                            'parameters': {
                                'type': 'object',
                                'properties': {
                                    'page': {
                                        'type': 'integer',
                                        'description': 'The page number of the help text to retrieve.',
                                    },
                                },
                                'required': ['page'],
                            },
                        },
                    },
                ],
            )
            
            self.history.append(response['message'])

            if not response['message'].get('tool_calls'):
                yield response['message']['content']
                break

            # Process tool calls
            for tool_call in response['message']['tool_calls']:
                tool_name = tool_call['function']['name']
                
                if tool_name in self.tools:
                    # Await the async tool function
                    result = await self.tools[tool_name](**tool_call['function']['arguments'])
                    
                    # Append the tool result to the history
                    self.history.append({
                        'role': 'tool',
                        'content': json.dumps(result) if isinstance(result, dict) else str(result),
                    })
                else:
                    print(f"Warning: Model tried to call unknown tool '{tool_name}'")
