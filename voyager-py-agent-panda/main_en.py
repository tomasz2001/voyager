import asyncio
from time import sleep
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import encode, Types
# import serial
import subprocess
import os
import signal


er_data = False


canisterId = 'p2137-cai'
glue_array = []

received_conn = ""
received_title = ""
received_conector = []

binfile = []

async def icpcon(metode, item1=None, item2=None, item3=None, item4=None, item5=None, item6=None, item7=None):
    global er_data, received_conn, received_title, received_conector
   
    ic_url = 'https://ic0.app'
    client = Client(url=ic_url)
    identity = Identity()
    agent = Agent(identity, client)

    try:

        if metode == 'file_one':
            param_file = [{'type': Types.Nat, 'value': item1}]
            result = await agent.query_raw_async(canisterId, "file_one", encode(param_file))

        if metode == 'glue':
            param_glue = [{'type': Types.Nat, 'value': glue_array}]
            result = await agent.query_raw_async(canisterId, "glue_get", encode(param_glue))

            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]

                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    return result_nice
                else:
                    print("Data error")
                    return None
            else:
                print("Data error")
                return None

        if metode == 'gluePUSH':
            param_glue = [{'type': Types.Vec(Types.Text), 'value': glue_array}]
            result = await agent.update_raw_async(canisterId, "glue_push", encode(param_glue))

            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]

                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    return result_nice
                else:
                    print("Data error")
                    return None
            else:
                print("Data error")
                return None

        if metode == 'help':
            param_query = [{'type': Types.Nat, 'value': int(item1)}]
            result = await agent.query_raw_async(canisterId, "help", encode(param_query))

            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]

                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    return result_nice
                else:
                    print("Data error")
                    return None
            else:
                print("Data error")
                return None

        if metode == 'hwoisme' or metode == 'getapp' or metode == 'getbox':
            if metode == 'getapp':
                param_query = [{'type': Types.Nat, 'value': int(item1)}]
                result = await agent.query_raw_async(canisterId, "conn_one", encode(param_query))
            elif metode == 'getbox':
                param_query = [{'type': Types.Nat, 'value': int(item1)}]
                result = await agent.query_raw_async(canisterId, "frend_one", encode(param_query))
            else:
                param_query = []
                result = await agent.query_raw_async(canisterId, "hwoisme", encode(param_query))

            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]
                
                if isinstance(first_element, dict) and 'value' in first_element:
                    conn_data = first_element['value']
                    
                    if isinstance(conn_data, dict):
                        global received_conn, received_title, received_conector
                        
                        values = list(conn_data.values())

                        if len(values) >= 3:
                            received_conn = str(values[0]) if isinstance(values[0], str) else ''
                            received_title = str(values[1]) if isinstance(values[1], str) else ''
                            received_conector = values[2] if isinstance(values[2], list) else []
                        else:
                            return False
                        
                        return True

            return None

        return None
    except Exception as e:
        print(f'Error: {e} ')
        er_data = True
        return None


async def monitor():
    global canisterId, received_conn, received_title, received_conector
    command = input("Command ready: ")
    if(command == "glue"):
        glue_array.clear()
        print("")
        while True:
            user_input = input("> ")
            if user_input.strip().lower() == "push":
                break
            if user_input.strip():
                glue_array.append(user_input)

        raport = await icpcon("glue", glue_array)
        print("")
        
        if(raport == "PUSH"):
            raport = await icpcon("gluePUSH", glue_array)
            print(raport)
            print("")
        else:
            print(raport)
            print("")

    elif(command == "target"):
        print("")
        canisterId = input("Enter the canister ID you want to interact with: ")

    elif(command == "hwoisme"):
        print("")
        raport = await icpcon("hwoisme")
        if raport == True:
            print("Conn data successfully received:")
            print(f"received_conn: {received_conn}")
            print(f"received_title: {received_title}")  
            print(f"received_conector: {received_conector}")
        else:
            print("Failed to receive Conn data.")
            print("")

    elif(command == "getapp"):
        print("")
        get = input("Enter index: ")
        print("")
        raport = await icpcon("getapp", get)
        if raport == True:
            print("Conn data successfully received:")
            print(f"received_conn: {received_conn}")
            print(f"received_title: {received_title}")  
            print(f"received_conector: {received_conector}")
        else:
            print("Failed to receive Conn data.")
            print("")

    elif(command == "getbox"):
        print("")
        get = input("Enter index: ")
        print("")
        raport = await icpcon("getbox", get)
        if raport == True:
            print("Conn data successfully received:")
            print(f"received_conn: {received_conn}")
            print(f"received_title: {received_title}")  
            print(f"received_conector: {received_conector}")
        else:
            print("Failed to receive Conn data.")
            print("")

    elif(command == "help"):
        print("")
        if(canisterId == "p2137-cai" or canisterId == ""):
            print("")
            print("hwoisme: check who you're talking to and what interfaces they expose")
            print("target: choose the canister you want to interact with")
            print("glue: use the glue interface with the selected target")
            print("help: show help")
            print("getbox: ask the databox about other databoxes")
            print("getapp: ask the databox about apps")
        else:
            line = input("Enter help page number for this service: ")
            raport = await icpcon("help", line)
            print(raport)
            print("")

    elif(command == "fileone"):
        print("The 'fileone' function is still under construction.")
        print("Thank you for using panda_voyager_agent.")

    else:
        print("Unsupported command.")


if __name__ == '__main__':
    print("")
    print("")
    print("[the panda] the simplest agent for Voyager")
    print("Have fun. If [you don't know] what to do,")
    print("type [help]")
    print("")
    print("")
    while True:
       asyncio.run(monitor())
