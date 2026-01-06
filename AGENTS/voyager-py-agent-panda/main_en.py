import asyncio
from time import sleep
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import encode, Types
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.backends import default_backend
from v_file import upload_file, download_file, check_file
# import serial
import subprocess
import os
import signal
import sys

identity_file = "identity.pem"

if os.path.exists(identity_file):
    with open(identity_file, "r") as f:
        private_key_pem = f.read().strip()
else:
    private_key_pem = ""

# Function to generate a new identity
def generate_new_identity():
    try:
        private_key = ed25519.Ed25519PrivateKey.generate()
        pem_pkcs8 = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')
        with open(identity_file, "w") as f:
            f.write(pem_pkcs8)
        print(f"New identity saved to {identity_file}", flush=True)
        return pem_pkcs8
    except Exception as e:
        print(f"Identity generation error: {e}", flush=True)
        return None

# Function to load identity
def load_identity_from_pem(pem_data):
    global private_key_pem
    try:
        if not pem_data or not pem_data.startswith("-----BEGIN PRIVATE KEY-----"):
            print("No key found, generating new identity...", flush=True)
            pem_data = generate_new_identity()
            if pem_data is None:
                return None
            private_key_pem = pem_data.strip()

        identity = Identity.from_pem(pem_data)
        return identity
    except Exception as e:
        print(f"Error loading identity: {e}", flush=True)
        return None


er_data = False


canisterId = 'p2137-cai'
glue_array = []

received_conn = ""
received_title = ""
received_conector = []

binfile = []

async def icpcon(method, item1=None, item2=None, item3=None, item4=None, item5=None, item6=None, item7=None):
    global er_data, received_conn, received_title, received_conector
   
    ic_url = 'https://ic0.app'
    client = Client(url=ic_url)
    identity = load_identity_from_pem(private_key_pem)
    agent = Agent(identity, client)    
    
    try:

        if method == 'glue':
            param_glue = [{'type': Types.Vec(Types.Text), 'value': glue_array}]
            result = await agent.query_raw_async(canisterId, "glue_get", encode(param_glue))

            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]
                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    return result_nice
                else:
                    print("data error")
                    return None
            else:
                print("data error")
                return None

        if method == 'gluePUSH':
            param_glue = [{'type': Types.Vec(Types.Text), 'value': glue_array}]
            result = await agent.update_raw_async(canisterId, "glue_push", encode(param_glue))

            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]
                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    return result_nice
                else:
                    print("data error")
                    return None
            else:
                print("data error")
                return None

        if method == 'help':
            param_query = [{'type': Types.Nat, 'value': int(item1)}]
            result = await agent.query_raw_async(canisterId, "help", encode(param_query))

            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]
                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    return result_nice
                else:
                    print("data error")
                    return None
            else:
                print("data error")
                return None
        

        if method in ['hwoisme', 'getapp', 'getbox']:
            if method == 'getapp':
                param_query = [{'type': Types.Nat, 'value': int(item1)}]
                result = await agent.query_raw_async(canisterId, "conn_one", encode(param_query))
            elif method == 'getbox':
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
                            received_title = str(values[0]) if isinstance(values[0], str) else ''
                            received_conn = str(values[1]) if isinstance(values[1], str) else ''
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
    command = input("command ready: ")
    if(command == "glue"):
        glue_array.clear()
        print("Enter data into the array, confirming each line with Enter.")
        print("When finished, type '@push' to send the array.")
        print("If you don't want to send, type '@break'.")
        print("")
        while True:
            user_input = input("> ")
            if user_input.strip().lower() == "@push":
                break
            if user_input.strip().lower() == "@break":
                glue_array.clear()
                break
            glue_array.append(user_input)
            
        if user_input == "@break":
            report = "Glue was broken and not sent."
        else:
            report = await icpcon("glue", glue_array)
            print("")
        
        if(report == "PUSH"):
            report = await icpcon("gluePUSH", glue_array)
            print(report)
            print("")
        else:
            print(report)
            print("")

    elif(command == "target"):
        print("")
        canisterId = input("enter canister ID you want to talk to: ")
    elif(command == "file"):
        try:
            print("")
            get = input(""" file commands

            upload : upload file
            download : download file
            check : check file in canister
            """)
            if(get == "upload"):
                up1 = input("file path : ")
                up2 = input("add file description : ")
                await upload_file(canisterId, up1, up2)

            elif(get == "download"):
                do1 = input("enter file index : ")
                await download_file(canisterId, do1)

            elif(get == "check"):
                do1 = input("enter file index : ")
                await check_file(canisterId, do1)
                
            else:
                print("unknown [file] command")
        except:
            print("file module encountered a problem")

    elif(command == "hwoisme"):
        print("")
        report = await icpcon("hwoisme")
        if report == True:
            print("Conn data successfully received:")
            print(f"received_conn: {received_conn}")
            print(f"received_title: {received_title}")  
            print(f"received_conector: {received_conector}")
        else:
            print("Failed to receive Conn data")
            print("")

    elif(command == "getapp"):
        print("")
        get = input("enter index: ")
        print("")
        report = await icpcon("getapp", get)
        if report == True:
            print("Conn data successfully received:")
            print(f"received_conn: {received_conn}")
            print(f"received_title: {received_title}")  
            print(f"received_conector: {received_conector}")
        else:
            print("Failed to receive Conn data")
            print("")

    elif(command == "getbox"):
        print("")
        get = input("enter index: ")
        print("")
        report = await icpcon("getbox", get)
        if report == True:
            print("Conn data successfully received:")
            print(f"received_conn: {received_conn}")
            print(f"received_title: {received_title}")  
            print(f"received_conector: {received_conector}")
        else:
            print("Failed to receive Conn data")
            print("")
        
    elif(command == "help"):
        print("");
        if(canisterId == "p2137-cai" or canisterId == ""):
            print("")
            print("hwoisme: check who you are talking to and what interfaces it has")
            print("target: choose the canister you want to talk to")
            print("glue: use the glue interface with the selected target")
            print("help: use the help interface")
            print("getbox: ask databox about other databoxy")
            print("getapp: ask databox about applications")
            print("file: upload or download file")
        else:
            line = input("enter help page number of this service")
            report = await icpcon("help", line)
            print(report)
            print("")

    else:
        print("unsupported command")


if __name__ == '__main__':
    print("")
    print("")
    print("[the panda] the simplest agent for voyager")
    print("enjoy your experience! if [you don't know] what to do,")
    print("type [help]")
    print("")
    print("")
    while True:
       asyncio.run(monitor())
# agent-panda 1.1 file,s edition
