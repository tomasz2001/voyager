import asyncio
from voyager_agent import VoyagerAgent

async def monitor():
    """Monitors for user input and interacts with the VoyagerAgent."""
    agent = VoyagerAgent()
    
    while True:
        prompt = input("> ")
        if prompt.lower() == 'exit':
            break
            
        print("Agent: ", end="", flush=True)
        final_response = ""
        async for chunk in agent.chat_with_tools(prompt):
            final_response += chunk
            print(chunk, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    print("""

[PANDA]

NAJPROSTRZY AGENT VOYAGER
NIE WIESZ CO I JAK WPISZ [help]
""")    
    while True:
       asyncio.run(monitor())