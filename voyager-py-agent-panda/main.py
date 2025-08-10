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
    print("")
    print("")
    print("[the panda] naiprosztrzy agnet do voyagera")
    print("zyczymy miłej zabawy jak [nie wiesz] co robić")
    print("wpisz [help]")
    print("")
    print("")
    while True:
       asyncio.run(monitor())