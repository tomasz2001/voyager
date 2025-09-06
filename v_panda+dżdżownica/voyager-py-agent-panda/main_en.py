import asyncio
from time import sleep
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import encode, Types
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.backends import default_backend
from golem_base_sdk import GenericBytes, GolemBaseClient

# import
import split
import subprocess
import os
import signal
import sys


# global value
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
        print(f"Error generating identity: {e}", flush=True)
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
        #print("Identity loaded", flush=True)
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

async def icpcon(metode, item1=None, item2=None, item3=None, item4=None, item5=None, item6=None, item7=None):
    global er_data, received_conn, received_title, received_conector
   
    ic_url = 'https://ic0.app'
    client = Client(url=ic_url)
    identity = load_identity_from_pem(private_key_pem)
    agent = Agent(identity, client)    
    
    try:

        if metode == 'file_one':
            param_file = [{'type': Types.Vec(Types.Text), 'value': glue_array}]
            result = await agent.query_raw_async(canisterId, "file_one", encode(param_file))


        if metode == 'glue':
            param_glue = [{'type': Types.Vec(Types.Text), 'value': glue_array}]
            result = await agent.query_raw_async(canisterId, "glue_get", encode(param_glue))


            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]

                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    #print(f'report: {result_nice}')
                    return result_nice
                else:
                    print("data error")
                    return None
            else:
                print("data error")
                return None

        
        if metode == 'gluePUSH':
            param_glue = [{'type': Types.Vec(Types.Text), 'value': glue_array}]
            
            result = await agent.update_raw_async(canisterId, "glue_push", encode(param_glue))



            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]

                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    #print(f'report: {result_nice}')
                    return result_nice
                else:
                    print("data error")
                    return None
            else:
                print("data error")
                return None


        if metode == 'help':
            param_query = [{'type': Types.Nat, 'value': int(item1)}]
            
            result = await agent.query_raw_async(canisterId, "help", encode(param_query))



            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]

                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    #print(f'report: {result_nice}')
                    return result_nice
                else:
                    print("data error")
                    return None
            else:
                print("data error")
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
                #print(f"First element: {first_element}")
                
                if isinstance(first_element, dict) and 'value' in first_element:
                    conn_data = first_element['value']
                    #print(f"Conn data: {conn_data}")
                    #print(f"Conn data type: {type(conn_data)}")
                    #print(f"Conn data keys: {conn_data.keys() if isinstance(conn_data, dict) else 'Not dict'}")
                    
                    if isinstance(conn_data, dict):
                        global received_conn, received_title, received_conector
                        
                        
                        values = list(conn_data.values())

                        if len(values) >= 3:
                            received_title = str(values[0]) if isinstance(values[0], str) else ''
                            received_conn = str(values[1]) if isinstance(values[1], str) else ''
                            received_conector = values[2] if isinstance(values[2], list) else []
                        else:
                            return False
                        #print(f'Received Conn structure:')
                        #print(f'conn: {received_conn}')
                        #print(f'title: {received_title}')
                        #print(f'conector: {received_conector}')
                        
                        return True

            return None

        return None
    except Exception as e:
        print(f'Error: {e} ')
        er_data = True
        return None

# worm function code
async def vdz_golem_one(target):

    client = await GolemBaseClient.create_ro_client(
        "https://ethwarsaw.holesky.golemdb.io/rpc", 
        "wss://ethwarsaw.holesky.golemdb.io/rpc/ws"
    )
    get = (await client.get_storage_value(GenericBytes.from_hex_string(target)))
    await client.disconnect()
    return get

async def get_vd_by_index(index=0):
    
    client = await GolemBaseClient.create_ro_client(
        "https://ethwarsaw.holesky.golemdb.io/rpc", 
        "wss://ethwarsaw.holesky.golemdb.io/rpc/ws"
    )
    vd_entities = await client.query_entities('type="vd"')
    
    if index < 0 or index >= len(vd_entities):
        await client.disconnect()
        return None

    entity = vd_entities[index]

    
    target_hash = entity.entity_key

    await client.disconnect()
    return target_hash




async def monitor():
    global canisterId, received_conn, received_title, received_conector
    command = input("command ready: ")
    if(command == "glue"):
        # glue test 
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
            raport = "Glue was broken and not sent."
        else:
            raport = await icpcon("glue", glue_array)
            print("");
        
        if(raport == "PUSH"):
            raport = await icpcon("gluePUSH", glue_array)
            print(raport)
            print("")
            
        else:
            print(raport)
            print("")

    elif(command == "target"):
        print("")
        canisterId = input("enter the canister of the service you want to interact with: ")

    elif(command == "hwoisme"):
        print("")
        raport = await icpcon("hwoisme")
        if raport == True:
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
        raport = await icpcon("getapp", get)
        if raport == True:
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
        raport = await icpcon("getbox", get)
        if raport == True:
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
            print("hwosime: check who you are talking to and their interfaces")
            print("target: choose the canister you want to interact with")
            print("glue: use the glue interface with the selected target")
            print("help: use help")
            print("getbox: ask a databox about other databoxes")
            print("getapp: ask a databox about applications")
            print("vo-dz: worm function currently on Golem-DB")
        else:
            line = input("enter the help page of this service")
            raport = await icpcon("help", line)
            print(raport)
            print("")
    elif(command == "fileone"):
        print("fileone function is still under construction")
        print("thank you for using panda_voyager_agent services")


    elif(command == "vo-dz"):
        target = input("choose target or type auto: ")
        print("") 
        if(target == "auto"):
            index = input("enter index [number] to search: ")
            target = await get_vd_by_index(int(index))
            print("Target hash: ", target)
            
        work = await vdz_golem_one(target)
        
        work = work.decode("utf-8")
        parts = work.split("/")

        a = parts[0]
        b = parts[1]  
        c = parts[2]
        print("")
        if(a != "vd"):
            print("WARNING! The data here may be incorrect or corrupted")
            print("")
        print("canister-databox-id: ", b)
        print("")
        print("previously defined record: ", c)
        
        while True:
            print("do you want to check the previously defined record: [yes/no]")
            qwery = input("if you want to set this databox as target, type [target]: ")
            print("")
            if(qwery == "yes"):
                target = c
                work = await vdz_golem_one(target)
        
                work = work.decode("utf-8")
                parts = work.split("/")

                a = parts[0]
                b = parts[1]  
                c = parts[2]
                print("canister-databox-id: ", b)
                print("")
                print("previous record hash: ", c)
                
            elif(qwery == "target"):
                canisterId = b
                break
            else:
                break

    else:
        print("command not supported")

    
if __name__ == '__main__':
    print("")
    print("")
    print("[the panda] simplest agent for voyager")
    print("have fun if [you don't know] what to do")
    print("type [help]")
    print("")
    print("")
    while True:
        asyncio.run(monitor())
