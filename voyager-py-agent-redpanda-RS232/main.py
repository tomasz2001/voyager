import serial
import time
import asyncio
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import encode, Types

# === Konfiguracja ===
PORT = '/dev/ttyACM0'
BAUDRATE = 9600
TIMEOUT = 1

# === Zmienne on-chain ===
canisterId = "mozdu-gyaaa-aaaae-aakoq-cai"

# === Inicjalizacja połączenia ===
arduino = serial.Serial(port=PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
time.sleep(2)  # Czekamy na reset Arduino

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

# === Inicjalizacja połączenia ===
async def send_response(response: str):
    if arduino.isOpen():
        arduino.write((response.strip() + '\n').encode())

# === Funkcje robocze ===
async def chip_function(command: str) -> str:
    return await icpcon("chip", command)


async def chip_up_function(command: str) -> str:
    return await icpcon("chip_up", command)

# === Router ===
async def route_command(command: str):
    if not command:
        return
    first_char, rest = command[0], command[1:].strip()
    if first_char == '?':
        result = await chip_function(rest)
    elif first_char == '^':
        result = await chip_up_function(rest)
    else:
        result = await chip_function(command.strip())
    await send_response(result)

# === Główna pętla ===
async def main_loop():
    try:
        while True:
            if arduino.in_waiting:
                line = arduino.readline().decode(errors='ignore').strip()
                if line:
                    print(f"[Arduino] Otrzymano: {line}")
                    await route_command(line)
            await asyncio.sleep(0.05)
    except asyncio.CancelledError:
        pass
    finally:
        if arduino.isOpen():
            arduino.close()
        print("[Python] Połączenie zamknięte.")

# === Start programu ===
if __name__ == '__main__':
    try:
        # asyncio.run() stworzy pętlę, wykona main_loop() i ją zamknie
        print("starting")
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\nPrzerwano przez użytkownika.")
    finally:
        if arduino.isOpen():
            arduino.close()
        print("[Python] Połączenie zamknięte.")