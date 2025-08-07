import serial
import time
import asyncio
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import encode, Types

# port config
#PORT = '/dev/ttyACM0'
#BAUDRATE = 9600
#TIMEOUT = 1

# canister conn
canisterId = "mh2ii-qqaaa-aaaae-aakpa-cai"


module_1 = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)
time.sleep(2)

async def icpcon(metode, item1=None):
    global er_data, received_conn, received_title, received_conector
    param_chip = [{'type': Types.Text, 'value': item1}]
    ic_url = 'https://ic0.app'
    client = Client(url=ic_url)
    identity = Identity()
    agent = Agent(identity, client)

    try:

        if metode == 'chip':
            
            result = await agent.query_raw_async(canisterId, "chip", encode(param_chip))

            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]

                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    print("raport : " + result_nice)
                    return result_nice
                else:
                    print("Data error")
                    return "dupa"
            else:
                print("Data error")
                return "dupa"

        if metode == 'chip_up':
            
            result = await agent.update_raw_async(canisterId, "chip_up", encode(param_chip))

            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]

                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    print("raport : " + result_nice)
                    return result_nice
                else:
                    print("Data error")
                    return "dupa"
            else:
                print("Data error")
                return "dupa"

        
        return "dupa"
    except Exception as e:
        print(f'Error: {e} ')
        er_data = True
        return "dupa"

# === conn ===
async def send_response(response: str):
    if module_1.isOpen():
        module_1.write((response.strip() + '\n').encode())

# === fukcjion work ===
#async def chip_function(command: str) -> str:
#    return ("chip", command)


#async def chip_up_function(command: str) -> str:
#    return await icpcon("chip_up", command)

# === fukcjion work ===
async def router_command(command: str):
    if not command:
        return
    first_char, rest = command[0], command[1:].strip()
    if first_char == '?':
        result = await icpcon("chip", rest)
    elif first_char == '^':
        result = await icpcon("chip_up", rest)
    else:
        result = await icpcon("chip", command.strip())
    await send_response(result)


async def main_loop():
    try:
        while True:
            if module_1.in_waiting:
                line = module_1.readline().decode(errors='ignore').strip()
                if line:
                    print(f"[module_1] Otrzymano: {line}")
                    await router_command(line)
            await asyncio.sleep(0.05)
    except asyncio.CancelledError:
        pass
    finally:
        if module_1.isOpen():
            module_1.close()
        print("[Python] Połączenie zamknięte.")


if __name__ == '__main__':
    try:

        print("starting")
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\nPrzerwano przez użytkownika.")
    finally:
        if module_1.isOpen():
            module_1.close()
        print("[Python] Połączenie zamknięte.")